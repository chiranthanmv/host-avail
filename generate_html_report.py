import os

def generate_html(all_results, timestamp_info, output_file='task_report.html'):
    timestamp = timestamp_info['results_ping']
    timestamp_section = f'<center><h3>Timestamp: {timestamp}</h3></center>' if timestamp else ''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Combined Task Report</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 80%;
                margin: auto;
                overflow: hidden;
            }}
            header {{
                background: #333;
                color: #fff;
                padding: 1rem 0;
                text-align: center;
            }}
            h1 {{
                margin: 0;
            }}
            .report {{
                background: #fff;
                padding: 2rem;
                margin: 1rem 0;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 1rem;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            .sucess-header {{
                background-color: #4CAF50;
                color: white;
            }}
            .failed-header {{
                background-color: #FF4C4C;
                color: white;
            }}
            tbody tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            h2 {{
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 0.5rem;
                margin-bottom: 1rem;
            }}
            h3 {{
                color: #555;
            }}
            center {{
                display: block;
                text-align: center;
                margin-bottom: 1rem;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Host Availability Report</h1>
        </header>
        {timestamp_section}
        <div class="container">
    '''

    for file_name, results in all_results.items():
        html_content += f'''
        <div class="report">
            <h2>Report for {file_name}</h2>
            <h3>Successful Pings</h3>
            <table>
                <thead>
                    <tr class="sucess-header">
                        <th>#</th>
                        <th>Hostname</th>
                    </tr>
                </thead>
                <tbody>
        '''
        if not results['success']:
            html_content += '''
                <tr>
                    <td colspan="2">No success</td>
                </tr>
            '''
        else:
            for index, task in enumerate(results['success']):
                html_content += f'''
                    <tr>
                        <td>{index+1}</td>
                        <td>{task}</td>
                    </tr>
                '''
        
        html_content += '''
                </tbody>
            </table>
            <h3>Failed Pings</h3>
            <table>
                <thead>
                    <tr class="failed-header">
                        <th>#</th>
                        <th>Hostname</th>
                    </tr>
                </thead>
                <tbody>
        '''

        if not results['failure']:
            html_content += '''
                <tr>
                    <td colspan="2">No success</td>
                </tr>
            '''
        else:
            for index, task in enumerate(results['failure']):
                html_content += f'''
                    <tr>
                        <td>{index+1}</td>
                        <td>{task}</td>
                    </tr>
                '''
        
        html_content += '''
                </tbody>
            </table>
        </div>
        '''

    html_content += '''
        </div>
    </body>
    </html>
    '''

    with open(output_file, 'w') as file:
        file.write(html_content)

def process_file(file_path):
    https_results = {
        'success': [],
        'failure': []
    }
    flag = 1
    timestamp = ''
    
    with open(file_path, 'r') as fs:
        fs_lines = fs.read().splitlines()

    fs_lines = list(filter(None, fs_lines))

    for line in fs_lines:
        if "Run at" in line:
            timestamp = line
        elif "Successful" in line:
            continue
        elif "Failed" in line:
            flag = 0
        elif not "Failed" in line and flag:
            https_results['success'].append(line.replace("- ", ""))
        else:
            https_results['failure'].append(line.replace("- ", ""))

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    return file_name, https_results, timestamp

# List of files to process
files_to_process = ['results_ping.log', 'results_http.log', 'results_https.log', 'results_ldap.log']
all_results = {}
timestamp_info = {}

for file_path in files_to_process:
    if os.path.exists(file_path):
        file_name, results, timestamp = process_file(file_path)
        all_results[file_name] = results
        timestamp_info[file_name] = timestamp
    else:
        print(f"File {file_path} does not exist.")

generate_html(all_results, timestamp_info)
