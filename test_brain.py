import requests
import json
import sys

# Configuration
URL = "http://localhost:7999/execute"
SESSION_ID = None

def send_commands(commands):
    global SESSION_ID
    payload = {"commands": commands}
    if SESSION_ID:
        payload["sessionId"] = SESSION_ID
    
    try:
        response = requests.post(URL, json=payload, timeout=30)
        resp = response.json()
        
        if resp.get("success"):
            SESSION_ID = resp.get("sessionId")
            return resp.get("output")
        else:
            return f"❌ Error: {resp.get('error')}"
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

def main():
    print("=== AlphaStS Interactive Test Terminal ===")
    print("Type 'exit' to quit, type 'help' for common sync commands")
    print("Recommended to input '0' for the first run to enter battle interface\n")

    while True:
        try:
            user_input = input("🎮 SpireAI > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break
                
            if user_input.lower() == "help":
                print("\n[Common Sync Commands]")
                print("  0             - Execute the first action in the list (usually Begin Battle)")
                print("  ph <number>   - Set player current HP (e.g., ph 50)")
                print("  pe <number>   - Set player current energy (e.g., pe 3)")
                print("  pb <number>   - Set player current block (e.g., pb 10)")
                print("  sh <cards...> - Sync hand cards (e.g., sh Strike,Strike,Defend)")
                print("  decide <steps>- Let AI think and return a RESULT index")
                print("  i             - View detailed information of current Java simulation")
                print("  reset         - Reset Java side state\n")
                continue

            # Send commands to Java
            output = send_commands([user_input])
            
            # Format output
            if "RESULT:" in output:
                # Highlight AI decision result
                parts = output.split(":")
                print(f"\n✨ AI Decision Result ✨")
                print(f"  Action Index: {parts[1]}")
                print(f"  Action Content: {parts[2]}")
                print(f"  Action Type: {parts[3]}")
                print("-" * 20)
            else:
                print(output)

        except KeyboardInterrupt:
            print("\nInterrupt detected, exiting...")
            break

if __name__ == "__main__":
    main()