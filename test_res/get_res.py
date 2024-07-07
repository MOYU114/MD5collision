import re

# Function to parse the text data
def parse_md5_collision_data(text):
    # Split text into sessions based on the repeated license information
    sessions = re.split(r"MD5 collision generator v\d+\.\d+", text)
    results = []
    times=[0,0,0,0,0]
    block_cnt=[0,0,0,0,0]
    # Process each session
    for session in sessions:
        if "用时" in session:
            time_taken_match = re.search(r"用时：([\d\.]+)", session)
            last_block_match = re.search(r"Generating second block: ([A-Z0-9]+)", session.split("\n")[-3])  # last used block line
            
            if time_taken_match and last_block_match:
                time_taken = float(time_taken_match.group(1))
                last_block = last_block_match.group(1)
                results.append({"time_taken": time_taken, "last_block": last_block})

                if(last_block=='W'):
                    block_cnt[0]+=1
                    times[0] += time_taken
                elif(last_block=='S00'):
                    block_cnt[1]+=1
                    times[1] += time_taken
                elif(last_block=='S01'):
                    block_cnt[2]+=1
                    times[2] += time_taken
                elif(last_block=='S10'):
                    block_cnt[3]+=1
                    times[3] += time_taken
                else:
                    block_cnt[4]+=1
                    times[4] += time_taken
    

    return results,times,block_cnt

# Load and read the file
file_path = 'res2.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# Parse the data
collision_results,times,block_cnt = parse_md5_collision_data(file_content)
for i in range(len(collision_results)):
    print(collision_results[i])
print(times)
print(block_cnt)