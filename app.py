import os
import json
import time
import requests
from datetime import timedelta
from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__, template_folder='templates')
app.secret_key = "out_of_law_super_secret_key" # Secure key for sessions

# --- Configurations ---
TARGET_LIMIT = 40
API_URL = "http://212.227.65.132:15279/player-info?uid="

# Admin Credentials
ADMIN_USER = "admin"
ADMIN_PASS = "12345"

FILES = {
    'active': 'active.json', 
    'profile': 'profile.json', 
    'history': 'history.json',
    'data': 'data.json', 
    'vv': 'vv.json', 
    'live': 'bots_live_status.json',
    'targets_txt': 'targets.txt', 
    'maintenance': 'maintenance.json'
}

def load_json(path, default):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f: json.dump(default, f, indent=4)
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    except: return default

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4)

def check_maintenance():
    return load_json(FILES['maintenance'], {"status": False, "end_time": 0}).get("status", False)

def init_files():
    for key, path in FILES.items():
        if key == 'vv': load_json(path, {"bot1": "pass1"})
        elif key == 'live': load_json(path, {})
        elif key == 'maintenance': load_json(path, {"status": False, "end_time": 0})
        elif key in ['profile', 'data']: load_json(path, {})
        elif key.endswith('.json'): load_json(path, [])

def add_history(action, uid, name):
    history = load_json(FILES['history'], [])
    history.insert(0, {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "action": action, "uid": uid, "name": name})
    save_json(FILES['history'], history[:100])

def distribute_targets():
    vv_data = load_json(FILES['vv'], {})
    active_data = load_json(FILES['active'], [])
    bot_count = len(vv_data)
    distribution = {}
    
    if bot_count > 0:
        for i in range(1, bot_count + 1): distribution[str(i)] = []
        for index, target in enumerate(active_data): 
            distribution[str((index % bot_count) + 1)].append(target['uid'])
            
    with open(FILES['targets_txt'], 'w', encoding='utf-8') as f: 
        json.dump(distribution, f, indent=4)

def check_expired_targets():
    if check_maintenance(): return
    active_data = load_json(FILES['active'], [])
    profiles = load_json(FILES['profile'], {})
    current_time = int(time.time() * 1000)
    
    new_active = []
    changed = False
    
    for t in active_data:
        if t['expireAt'] == 'permanent' or int(t['expireAt']) > current_time: 
            new_active.append(t)
        else:
            changed = True
            add_history("Expired", t['uid'], t['name'])
            if t['uid'] in profiles: 
                del profiles[t['uid']]
                
    if changed:
        save_json(FILES['active'], new_active)
        save_json(FILES['profile'], profiles)
        distribute_targets()

def fetch_and_parse_ff_api(uid):
    try:
        resp = requests.get(f"{API_URL}{uid}", timeout=15)
        raw_data = resp.json()
        
        if resp.status_code == 200 and "error" not in raw_data:
            basic = raw_data.get("basicInfo") or raw_data.get("basic_info") or {}
            clan = raw_data.get("clanBasicInfo") or raw_data.get("clan_basic_info") or {}
            social = raw_data.get("socialInfo") or raw_data.get("social_info") or {}
            
            data = {
                "basicInfo": {
                    "nickname": basic.get("nickname", "Unknown"), 
                    "level": basic.get("level", 0),
                    "headPic": basic.get("headPic") or basic.get("head_pic") or 902000003,
                    "bannerId": basic.get("bannerId") or basic.get("banner_id") or 901000001,
                    "region": basic.get("region", "N/A"), 
                    "liked": basic.get("liked", 0),
                    "createAt": basic.get("createAt") or basic.get("create_at") or 0,
                    "lastLoginAt": basic.get("lastLoginAt") or basic.get("last_login_at") or 0
                },
                "clanBasicInfo": {
                    "clanName": clan.get("clanName") or clan.get("clan_name") or "No Guild", 
                    "captainId": clan.get("captainId") or clan.get("captain_id") or "N/A"
                },
                "socialInfo": {
                    "signature": social.get("signature", "Default Signature")
                }
            }
            return {"success": True, "data": data}
            
        return {"success": False, "msg": raw_data.get("error", "API Error")}
    except Exception as e: 
        return {"success": False, "msg": str(e)}

init_files()

# ==========================================
# --- ROUTES ---
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        remember = request.form.get('remember')
        
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session['logged_in'] = True
            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            else:
                session.permanent = False
            return redirect(url_for('index'))
        else:
            return render_template('index.html', show_login=True, error="Invalid Credentials!")
    
    if session.get('logged_in'): 
        return redirect(url_for('index'))
    return render_template('index.html', show_login=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('logged_in'): 
        return redirect(url_for('login'))
    return render_template('index.html', show_login=False)

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    if not session.get('logged_in'): 
        return jsonify({"error": "Unauthorized"}), 401
        
    check_expired_targets()
    active_targets = load_json(FILES['active'], [])
    live_bots = load_json(FILES['live'], {})
    
    bots_list = [
        {
            "no": i+1, 
            "name": d.get("Name", "Unknown"), 
            "uid": d.get("Game uid", "N/A"), 
            "status": d.get("Status", "Offline")
        } for i, (b, d) in enumerate(live_bots.items())
    ]
    return jsonify({"total_targets": len(active_targets), "total_bots": len(bots_list), "bots": bots_list})

@app.route('/api/targets', methods=['GET'])
def get_targets():
    if not session.get('logged_in'): 
        return jsonify([]), 401
        
    check_expired_targets()
    targets = load_json(FILES['active'], [])
    profiles = load_json(FILES['profile'], {})
    
    for t in targets:
        p_basic = profiles.get(t['uid'], {}).get('basicInfo', {})
        p_clan = profiles.get(t['uid'], {}).get('clanBasicInfo', {})
        
        t['headPic'] = p_basic.get('headPic', '902000003')
        t['level'] = p_basic.get('level', 0)
        t['liked'] = p_basic.get('liked', 0)
        t['region'] = p_basic.get('region', 'N/A')
        t['guild'] = p_clan.get('clanName', 'No Guild')
        
    return jsonify(targets)

@app.route('/api/fetch_profile', methods=['POST'])
def fetch_profile():
    """
    Fetches target profile data.
    Takes an optional boolean "save" flag (default True).
    If save=False, it fetches from API but does not save in profile.json
    (Useful for fetching Leader profiles)
    """
    if not session.get('logged_in'): 
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    data = request.get_json(force=True)
    uid = str(data.get('uid')).strip()
    save_profile = data.get('save', True)
    force_refresh = data.get('force', False)
    
    profiles = load_json(FILES['profile'], {})
    
    # Return from cache if we don't need to force refresh and data exists
    if not force_refresh and uid in profiles: 
        return jsonify({"success": True, "data": profiles[uid]})
        
    api_res = fetch_and_parse_ff_api(uid)
    
    # Save only if it's a successful target fetch and save flag is True
    if api_res["success"] and save_profile:
        profiles[uid] = api_res["data"]
        save_json(FILES['profile'], profiles)
        
    return jsonify(api_res)

@app.route('/api/target/add', methods=['POST'])
def add_target():
    if not session.get('logged_in'): 
        return jsonify({"success": False, "msg": "Unauthorized"})
        
    data = request.get_json(force=True)
    uid = str(data.get('uid')).strip()
    reason = data.get('reason', '')
    duration_str = data.get('duration', '1 day')
    
    active_data = load_json(FILES['active'], [])
    if len(active_data) >= TARGET_LIMIT:
        return jsonify({"success": False, "msg": f"Target limit ({TARGET_LIMIT}) reached!"})
        
    if any(t['uid'] == uid for t in active_data): 
        return jsonify({"success": False, "msg": "Target already exists."})
    
    api_res = fetch_and_parse_ff_api(uid)
    if not api_res["success"]: 
        return jsonify({"success": False, "msg": api_res["msg"]})
        
    current_time = int(time.time() * 1000)
    durations = {
        '1 day': 86400000, '2 day': 86400000*2, '3 day': 86400000*3, 
        '7 day': 86400000*7, '30 day': 86400000*30
    }
    expire_at = 'permanent' if duration_str == 'permanent' else current_time + durations.get(duration_str, 86400000)

    active_data.append({
        "id": f"t_{current_time}", 
        "uid": uid, 
        "name": api_res["data"]["basicInfo"].get("nickname", "Unknown"),
        "reason": reason, 
        "duration": duration_str, 
        "addTime": current_time, 
        "expireAt": expire_at,
        "addedByName": ADMIN_USER, 
        "addedByRole": "Admin"
    })
    
    save_json(FILES['active'], active_data)
    
    profiles = load_json(FILES['profile'], {})
    profiles[uid] = api_res["data"]
    save_json(FILES['profile'], profiles)
    
    distribute_targets()
    return jsonify({"success": True, "msg": "Protocol active on target!"})

@app.route('/api/target/delete', methods=['POST'])
def delete_target():
    if not session.get('logged_in'): 
        return jsonify({"success": False, "msg": "Unauthorized"})
        
    uid = request.json.get('uid')
    active_data = load_json(FILES['active'], [])
    new_active = [t for t in active_data if t['uid'] != uid]
    
    if len(new_active) != len(active_data):
        save_json(FILES['active'], new_active)
        distribute_targets()
        return jsonify({"success": True})
        
    return jsonify({"success": False, "msg": "Target not found."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20571, debug=True)