from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, send_file
from flask_mail import Mail, Message
from fpdf import FPDF
import io
import os
import requests 
import shodan # NEW: Added Shodan library
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-change-me')

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# Initialize Shodan Client
SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')
shodan_api = shodan.Shodan(SHODAN_API_KEY) if SHODAN_API_KEY else None

# --- Data ---
PERSONAL_INFO = {
    "name": "Pradip Pandey", 
    "title": "Digital Engagement Officer & Cybersecurity Specialist",
    "tagline": "Bridging the gap between complex IT infrastructure and community digital literacy.",
    "summary": "I am a versatile IT professional with a unique blend of cybersecurity expertise and hands‑on technical support experience. My background spans network engineering, system administration, hardware/software troubleshooting, and end‑user support — making me an adaptable asset to any IT team.",
    "email": "pradippandey555@gmail.com",
    "github": "pradippandey555",
    "linkedin": "pradip-pandey-317997195"
}

SKILLS_DATA = [
    {
        "category": "Operating Systems",
        "icon": "fa-desktop",
        "color": "border-green-500",
        "items": [
            "Windows Server 2019/2022: AD, Group Policy, DNS, DHCP",
            "Windows 10/11 installation, administration & troubleshooting",
            "Linux (Ubuntu, CentOS): Server config, shell scripting",
            "macOS basic administration & cross‑platform support"
        ]
    },
    {
        "category": "Networking & Security",
        "icon": "fa-network-wired",
        "color": "border-blue-500",
        "items": [
            "Cisco routing & switching: VLANs, OSPF, EIGRP, ACLs",
            "Firewall configuration: Windows Firewall, Cisco ASA basics",
            "VPN setup: Site‑to‑site & remote access",
            "Access control in Microsoft environments",
            "Network monitoring (SIEM, NetFlow)",
            "Endpoint protection & security hardening"
        ]
    },
    {
        "category": "Virtualization & Cloud",
        "icon": "fa-cloud",
        "color": "border-purple-500",
        "items": [
            "VMware & VirtualBox lab creation",
            "Hyper‑V basics",
            "Azure & AWS fundamentals (VMs, storage, RBAC)",
            "VM deployment, snapshots, optimisation"
        ]
    },
    {
        "category": "Programming & Development",
        "icon": "fa-code",
        "color": "border-orange-500",
        "items": [
            "Python automation, log parsing, CSV data processing",
            "JavaScript, HTML5, CSS3 for responsive design",
            "Flask web app development & deployment",
            "Secure coding aligned with OWASP Top 10"
        ]
    },
    {
        "category": "IT Support & Troubleshooting",
        "icon": "fa-headset",
        "color": "border-indigo-500",
        "items": [
            "Level 1 & 2 help desk support",
            "Incident logging & resolution tracking",
            "Hardware diagnostics, repairs, maintenance",
            "Peripheral & network device configuration",
            "Software installation & version management"
        ]
    },
    {
        "category": "IT & Cybersecurity Management",
        "icon": "fa-shield-halved",
        "color": "border-red-500",
        "items": [
            "Risk assessment & security policy development",
            "Incident response planning & reporting",
            "System analysis & SDLC documentation",
            "IT asset lifecycle management & compliance"
        ]
    },
    {
        "category": "Soft Skills",
        "icon": "fa-people-group",
        "color": "border-teal-500",
        "items": [
            "Clear communication & customer service",
            "Problem‑solving under time pressure",
            "Adaptability across technologies",
            "Collaborative teamwork & knowledge sharing"
        ]
    }
]

CERTIFICATES = [
    { 
        "id": 1, 
        "title": "Network Analysis Using Wireshark 3", 
        "issuer": "Network Security", 
        "src": "Wireshark 3.jpg",
        "description": "Practical packet capture and traffic analysis skills."
    },
    { 
        "id": 2, 
        "title": "Wireless Penetration Using Kali Linux", 
        "issuer": "Penetration Testing", 
        "src": "Kali Wireless Pen Test.jpg",
        "description": "Hands‑on wireless network auditing and security testing."
    },
    { 
        "id": 3, 
        "title": "Cyber Security Fundamentals", 
        "issuer": "Cyber Security", 
        "src": "Cyber.jpg",
        "description": "Core concepts in security frameworks and risk mitigation."
    },
    { 
        "id": 4, 
        "title": "Metasploit Testing Recipes", 
        "issuer": "Vulnerability Assessment", 
        "src": "Metasploit Testing Recipes.jpg",
        "description": "Exploitation and vulnerability assessment techniques."
    },
    { 
        "id": 5, 
        "title": "Outlook Essentials", 
        "issuer": "Productivity", 
        "src": "Outlook.jpg",
        "description": "Efficient email, calendar, and task management skills."
    },
    { 
        "id": 6, 
        "title": "Network Scanning With NMAP", 
        "issuer": "Network Recon", 
        "src": "Network Scanning With NMAP.jpg",
        "description": "Proficiency in network reconnaissance and mapping."
    },
    { 
        "id": 7, 
        "title": "Comptia Network Certification Exam Essentials", 
        "issuer": "Networking", 
        "src": "Comptia Network Certification Exam Essentials.jpg",
        "description": "Fundamental networking knowledge and exam preparation."
    }
]

EDUCATION = [
    {
        "degree": "Bachelor of Cybersecurity (Current)",
        "institution": "Charles Sturt University",
        "year": "2023 - Present (2nd Year Completed)",
        "details": "Advanced focus on Digital Forensics, Network Security, and System Analysis. Consistent high achiever in Programming Principles and Database Systems.",
        "tags": ["Digital Forensics", "Network Defense", "System Analysis"]
    },
    {
        "degree": "Diploma of Information Technology (Networking)",
        "institution": "TAFE NSW",
        "year": "2022",
        "details": "Specialized in advanced network configuration, server management (Windows/Linux), and cybersecurity management protocols.",
        "tags": ["Cisco Networking", "Server Admin", "Virtualization"]
    },
    {
        "degree": "Certificate IV in Information Technology",
        "institution": "TAFE NSW",
        "year": "2021",
        "details": "Foundation in IT support, web development, and database administration.",
        "tags": ["Web Dev", "IT Support", "SQL"]
    },
    {
        "degree": "Certificate III in Information, Digital Media & Technology",
        "institution": "TAFE NSW",
        "year": "2020",
        "details": "Entry-level desktop support and operating system fundamentals.",
        "tags": ["Desktop Support", "OS Config"]
    }
]

PROJECTS = [
    {
        "id": 1,
        "title": "Hydra & Metasploitable Penetration Test",
        "role": "Penetration Tester",
        "category": "Cybersecurity",
        "description": "Executed brute-force attacks using Hydra against various services (SSH, FTP, HTTP) hosted on a Metasploitable 2 lab environment. Analyzed password strength vulnerabilities and implemented account lockout policies to mitigate dictionary attacks.",
        "tech": ["Hydra", "Metasploitable 2", "Brute-Force", "Password Auditing"],
        "icon": "fa-user-secret",
        "color": "border-red-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555/IT-Projects-Portfolio/tree/main/01_Hydra_PenTest",
        "guide_file": "1.md"
    },
    {
        "id": 2,
        "title": "Cloud Infrastructure Lab (Azure/AWS)",
        "role": "Cloud Engineer",
        "category": "Cloud & Virtualization",
        "description": "Designed and deployed a hybrid cloud architecture. Configured Azure VNETs and AWS VPCs with peering. Implemented NSGs (Network Security Groups) and IAM roles for least-privilege access control. Deployed load-balanced web servers.",
        "tech": ["Azure", "AWS", "VNET/VPC", "IAM", "Load Balancing"],
        "icon": "fa-cloud",
        "color": "border-blue-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555/IT-Projects-Portfolio/tree/main/02_Cloud_Lab",
        "guide_file": "2.md"
    },
    {
        "id": 3,
        "title": "Enterprise Switching & Routing (TAFE)",
        "role": "Network Engineer",
        "category": "Networking",
        "description": "Configured complex OSPF and EIGRP routing protocols for a multi-branch network topology. Implemented VLANs with Inter-VLAN routing (Router-on-a-Stick) and secured Layer 2 with Port Security and DHCP Snooping.",
        "tech": ["Cisco IOS", "OSPF", "EIGRP", "VLANs", "Port Security"],
        "icon": "fa-network-wired",
        "color": "border-orange-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555/IT-Projects-Portfolio/tree/main/03_Cisco_Network",
        "guide_file": "3.md"
    },
    {
        "id": 4,
        "title": "Digital Forensics Investigation (CSU)",
        "role": "Forensic Analyst",
        "category": "Cybersecurity",
        "description": "Conducted a forensic analysis of a compromised disk image using Autopsy and FTK Imager. Recovered deleted artifacts, analyzed registry keys for persistence mechanisms, and generated a legal-grade chain of custody report.",
        "tech": ["Autopsy", "FTK Imager", "Registry Analysis", "Chain of Custody"],
        "icon": "fa-magnifying-glass",
        "color": "border-purple-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555/IT-Projects-Portfolio/tree/main/04_Digital_Forensics",
        "guide_file": "4.md"
    },
    {
        "id": 5,
        "title": "Linux Server Hardening & Administration",
        "role": "SysAdmin",
        "category": "Operating Systems",
        "description": "Deployed Ubuntu servers and applied CIS Benchmark hardening standards. Configured SSH key-based auth, UFW firewall rules, and automated log monitoring with Fail2Ban to block repeated failed login attempts.",
        "tech": ["Linux (Ubuntu)", "Fail2Ban", "UFW", "SSH Hardening"],
        "icon": "fa-server",
        "color": "border-green-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555/IT-Projects-Portfolio/tree/main/05_Linux_Hardening",
        "guide_file": "5.md"
    },
    {
        "id": 6,
        "title": "Win Server AD & Group Policy Mgmt",
        "role": "Network Admin",
        "category": "Networking",
        "description": "Built a Windows Server 2019 Domain Controller. Configured Active Directory Users & Computers (ADUC), DNS, and DHCP. Deployed Group Policy Objects (GPOs) to enforce password complexity and disable USB storage devices.",
        "tech": ["Active Directory", "Group Policy", "DNS/DHCP", "Windows Server"],
        "icon": "fa-windows",
        "color": "border-blue-400/50",
        "youtube_id": "",
        "github_url": "https://github.com/pradippandey555/IT-Projects-Portfolio/tree/main/06_Windows_AD",
        "guide_file": "6.md"
    },
    {
        "id": 7,
        "title": "IT Project Management Simulation",
        "role": "Project Manager",
        "category": "Management",
        "description": "Led a simulated enterprise IT upgrade project. Utilized Waterfall/Agile methodologies to track milestones. Created Gantt charts, risk matrices, and stakeholder communication plans for a seamless data center migration.",
        "tech": ["Agile", "Waterfall", "Risk Mgmt", "Gantt Charts"],
        "icon": "fa-diagram-project",
        "color": "border-teal-500/50",
        "youtube_id": "",
        "github_url": "https://github.com/pradippandey555/IT-Projects-Portfolio/tree/main/07_Project_Management",
        "guide_file": "7.md"
    },
    {
        "id": 8,
        "title": "Mock Help Desk & Support Lab",
        "role": "Support Lead",
        "category": "IT Support",
        "description": "Managed a mock L1/L2 service desk queue. Resolved tickets related to hardware failures, OS corruption, and printer connectivity. Documented knowledge base (KB) articles for common issue resolution.",
        "tech": ["Ticket Mgmt", "Troubleshooting", "KB Creation", "SLA Mgmt"],
        "icon": "fa-headset",
        "color": "border-indigo-500/50",
        "youtube_id": "", 
        "github_url": "https://github.com/pradippandey555/IT-Projects-Portfolio/tree/main/08_Help_Desk",
        "guide_file": "8.md"
    }
]

# Route Definitions
@app.route('/')
def home():
    return render_template('home.html', 
                           personal_info=PERSONAL_INFO,
                           skills=SKILLS_DATA,
                           projects=PROJECTS,
                           certificates=CERTIFICATES,
                           education=EDUCATION)

@app.route('/annapurna')
def annapurna():
    return render_template('annapurna.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)


@app.route('/project/<int:project_id>/pdf')
def generate_pdf(project_id):
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- Cover Page ---
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 40, txt="", ln=True) # Spacer
    pdf.cell(0, 10, txt="Project Lab Manual", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(30, 64, 175) # Blue
    pdf.multi_cell(0, 10, txt=f"{project['title']}", align='C')
    pdf.set_text_color(0, 0, 0) # Reset Black
    
    pdf.ln(20)
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, f"Role: {project['role']}", ln=True, align='C')
    pdf.cell(0, 10, f"Category: {project['category']}", ln=True, align='C')
    
    pdf.ln(40)
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "Generated by Bright Rays Portfolio", ln=True, align='C')
    pdf.add_page()
    
    # --- Content Logic ---
    content = ""
    guide_path = os.path.join(app.root_path, 'lab_guides', project.get('guide_file', ''))
    if os.path.exists(guide_path):
        with open(guide_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            
            if line.startswith('# '):
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 16)
                pdf.set_text_color(30, 64, 175)
                pdf.cell(0, 10, line.replace('# ', ''), ln=True)
                pdf.set_text_color(0, 0, 0)
            elif line.startswith('## '):
                pdf.ln(4)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, line.replace('## ', ''), ln=True)
            elif line.startswith('### '):
                pdf.ln(2)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, line.replace('### ', ''), ln=True)
            elif line.startswith('* ') or line.startswith('- '):
                pdf.set_font("Arial", size=11)
                pdf.set_x(15) 
                pdf.multi_cell(0, 6, chr(149) + " " + line[2:])
            elif line.startswith('`') or line.startswith('    '):
                 pdf.set_font("Courier", size=10)
                 pdf.set_fill_color(240, 240, 240)
                 pdf.multi_cell(0, 5, line.replace('`', ''), fill=True)
            else:
                if line:
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 6, line)
                    pdf.ln(1)
    else:
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Detailed Lab Guide content not found.", ln=True)

    pdf.set_y(-15)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, f"Page {pdf.page_no()}", align='C')

    pdf_buffer = io.BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin-1', errors='replace')
    pdf_buffer.write(pdf_output)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"{project['title'].replace(' ', '_')}_Lab_Manual.pdf",
        mimetype='application/pdf'
    )

@app.route('/submit-help-request', methods=['POST'])
def submit_help_request():
    if request.method == 'POST':
        name = request.form.get('name')
        arrival_date = request.form.get('arrival_date')
        contact_info = request.form.get('contact_info')
        message = request.form.get('message')
        
        try:
            msg = Message(f"New Help Request from {name}",
                          recipients=['annapurnaaspirations@gmail.com'])
            msg.body = f"""
            Name: {name}
            Arrival Date: {arrival_date}
            Contact Info: {contact_info}
            Message: {message}
            """
            mail.send(msg)
            flash("Your request has been sent successfully!", "success")
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("There was an error sending your request. Please try again later.", "error")
            
        return redirect(url_for('annapurna'))

@app.route('/api/terminal', methods=['POST'])
def handle_terminal_command():
    data = request.get_json()
    user_command = data.get('command', '').strip()
    
    if not user_command:
        return jsonify({"response": "Error: No command provided."}), 400

    if user_command.lower() == "check_cyberagent_status":
        return jsonify({"response": "SYSTEM STATUS: ONLINE. Threat APIs connected."})
    
    # --- LIVE SHODAN INTEGRATION ---
    if user_command.lower().startswith("shodan "):
        if not shodan_api:
            return jsonify({"response": "[ERROR] SHODAN_API_KEY is missing from .env configuration."})
            
        ip_to_scan = user_command[7:].strip()
        try:
            # Query Shodan
            host = shodan_api.host(ip_to_scan)
            
            # Format the live response for the terminal
            response_text = f"[INFO] Target IP: {ip_to_scan}\n"
            response_text += f"[ORG] {host.get('org', 'Unknown')}\n"
            response_text += f"[OS] {host.get('os', 'Unknown')}\n"
            
            ports = host.get('ports', [])
            response_text += f"[PORTS] {', '.join(str(p) for p in ports)}\n\n"
            
            vulns = host.get('vulns', [])
            if vulns:
                response_text += f"[WARNING] {len(vulns)} CVEs detected.\n"
                for vuln in vulns[:5]: # Limit to top 5 to avoid flooding terminal
                    response_text += f" - {vuln}\n"
            else:
                response_text += "[RESULT] No known CVEs detected by Shodan.\n"
                
            return jsonify({"response": response_text})
            
        except shodan.APIError as e:
            return jsonify({"response": f"[ERROR] Shodan API Error: {str(e)}"})

        # --- AI DISABLED FOR PRODUCTION ---
    return jsonify({"response": "[INFO] Cyber Agent AI is currently in maintenance mode. Only Shodan scanning is available."})

    # --- LOCAL LLAMA FALLBACK ---
    """
    try:
        ollama_url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3", 
            "system": "You are 'CyberTutor', an advanced SOC Analyst AI operating inside a secure command-line terminal. Your responses must be concise, highly technical, and strictly formatted as raw terminal output. CRITICAL RULES: 1. NEVER use markdown formatting (no asterisks *, no bolding **, no hashtags #). 2. Never use conversational filler like 'Here is the analysis'. 3. Structure your data using strictly bracketed prefixes like [INFO], [ANALYSIS], [WARNING], or [RESULT].",
            "prompt": user_command,
            "stream": False
        }
        
        ai_response = requests.post(ollama_url, json=payload)
        ai_data = ai_response.json()
        
        final_text = ai_data.get("response", "Error: AI failed to generate a response.")
        return jsonify({"response": final_text})
        
    except requests.exceptions.ConnectionError:
        return jsonify({"response": "[CRITICAL ERROR] Local AI engine (Ollama) is offline."}), 503
    except Exception as e:
        return jsonify({"response": f"[SYSTEM FAULT] {str(e)}"}), 500
    """

if __name__ == '__main__':
    app.run(debug=False, port=3000)