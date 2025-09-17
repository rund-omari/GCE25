import streamlit as st
from pathlib import Path
import base64
import time

#------> paths
SOUNDS = Path("sounds")
IMAGES = Path("images")
TOTAL_ROOMS = 5
PER_ROOM_SECONDS = 30

#-----> q&a
RIDDLES = [
    {"room":1, "question":"What Is The Most Popular Search Engine?", "answers":["Google"]},
    {"room":2, "question":"What Is The Most Popular Mobile Operating System?", "answers":["Android"]},
    {"room":3, "question":"What Is The Most Popular Computer Operating System ?", "answers":["Windows"]},
    {"room":4, "question":"What Is The Name of The Device That Provides Internet To The Home?", "answers":["Router"]},
    {"room":5, "question":"What is the abbreviation for the processor in a computer?", "answers":["CPU"]},
]

def normalize(s: str) -> str:
    if s is None:
        return ""
    return str(s).strip().lower() 

#------> sounds player
def play_sound_file(path: Path):
    if path.exists():
        b = path.read_bytes()
        b64 = base64.b64encode(b).decode()
        mime = "audio/mpeg" if path.suffix.lower() in [".mp3",".mpeg"] else "audio/wav"
        st.components.v1.html(f'<audio autoplay><source src="data:{mime};base64,{b64}" type="{mime}"></audio>', height=0)

def play_correct_sound_and_proceed(path: Path):
  
    if path.exists():
        b = path.read_bytes()
        b64 = base64.b64encode(b).decode()
        mime = "audio/mpeg" if path.suffix.lower() in [".mp3",".mpeg"] else "audio/wav"
        
        # HTML+ javascript sound player
        html_with_delay = f'''
        <audio id="correctSound" autoplay>
            <source src="data:{mime};base64,{b64}" type="{mime}">
        </audio>
        <script>
            const audio = document.getElementById('correctSound');
            audio.onended = function() {{
                setTimeout(function() {{
                    window.parent.postMessage({{type: 'streamlit:rerun'}}, '*');
                }}, 200);
            }};
            // في حالة عدم وجود حدث onended، استخدم timeout
            setTimeout(function() {{
                window.parent.postMessage({{type: 'streamlit:rerun'}}, '*');
            }}, 2000);
        </script>
        '''
        st.components.v1.html(html_with_delay, height=0)

#------> image display functions(x)
def get_image_base64(image_path: Path):
    if image_path.exists():
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def display_door_image(door_state="closed", room_number=1):
    if door_state == "closed":
        door_svg = '''
        <div style="text-align: center; margin: 20px 0;">
            <div style="display: inline-block; padding: 20px; background: linear-gradient(135deg, #8B4513, #A0522D); border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.3); border: 3px solid #795548;">
                <svg width="300" height="400" viewBox="0 0 300 400" xmlns="http://www.w3.org/2000/svg">
                    <rect x="20" y="20" width="260" height="360" fill="#8B4513" stroke="#5D2F0A" stroke-width="3" rx="10"/>
                    <rect x="40" y="40" width="220" height="320" fill="#A0522D" stroke="#654321" stroke-width="2" rx="5"/>
                    <rect x="60" y="80" width="180" height="80" fill="none" stroke="#654321" stroke-width="2" rx="5"/>
                    <rect x="60" y="200" width="180" height="80" fill="none" stroke="#654321" stroke-width="2" rx="5"/>
                    <circle cx="220" cy="200" r="8" fill="#FFD700" stroke="#B8860B" stroke-width="2"/>
                    <rect x="200" y="180" width="15" height="10" fill="#C0C0C0" stroke="#808080" stroke-width="1" rx="2"/>
                    <text x="150" y="350" font-family="Arial" font-size="24" fill="#654321" text-anchor="middle">🔒</text>
                </svg>
            </div>
        </div>
        '''
        st.markdown(door_svg, unsafe_allow_html=True)
    else:
        specific_door = IMAGES / f"door_{door_state}_room_{room_number}.png"
        generic_door = IMAGES / f"door_{door_state}.png"
        door_path = specific_door if specific_door.exists() else generic_door
        
        if door_path.exists():
            img_base64 = get_image_base64(door_path)
            if img_base64:
                img_html = f'''
                <div style="text-align: center; margin: 20px 0;">
                    <img src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: 300px; object-fit: contain; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.3); border: 3px solid #4CAF50;">
                </div>
                '''
                st.markdown(img_html, unsafe_allow_html=True)
        else:
            open_door_svg = '''
            <div style="text-align: center; margin: 20px 0;">
                <div style="display: inline-block; padding: 20px; background: linear-gradient(135deg, #4CAF50, #45a049); border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.3); border: 3px solid #4CAF50;">
                    <svg width="300" height="400" viewBox="0 0 300 400" xmlns="http://www.w3.org/2000/svg">
                        <rect x="20" y="20" width="260" height="360" fill="#8B4513" stroke="#5D2F0A" stroke-width="3" rx="10"/>
                        <path d="M 40 40 L 200 60 L 200 340 L 40 360 Z" fill="#A0522D" stroke="#654321" stroke-width="2"/>
                        <path d="M 60 90 L 180 100 L 180 160 L 60 150 Z" fill="none" stroke="#654321" stroke-width="2"/>
                        <path d="M 60 210 L 180 220 L 180 280 L 60 270 Z" fill="none" stroke="#654321" stroke-width="2"/>
                        <circle cx="180" cy="200" r="6" fill="#FFD700" stroke="#B8860B" stroke-width="2"/>
                        <rect x="200" y="40" width="60" height="320" fill="#000080" opacity="0.3"/>
                        <text x="150" y="350" font-family="Arial" font-size="24" fill="#4CAF50" text-anchor="middle">🔓</text>
                    </svg>
                </div>
            </div>
            '''
            st.markdown(open_door_svg, unsafe_allow_html=True)

def reset_timer():
    st.session_state.start_time = time.time()

def time_left():
    return max(0, int(PER_ROOM_SECONDS - (time.time() - st.session_state.start_time)))

def next_room():
    st.session_state.room_id += 1
    st.session_state.show_open_door = False
    st.session_state.answer_checked = False  
    reset_timer()

def reset_game():
    st.session_state.room_id = 0
    st.session_state.game_started = False
    st.session_state.game_over = False
    st.session_state.win_shown = False
    st.session_state.lose_shown = False
    st.session_state.show_open_door = False
    st.session_state.answer_checked = False
    reset_timer()

def main():
    st.set_page_config(page_title="Answer To Escape", page_icon="🗝️")

#---> var  
    if "room_id" not in st.session_state:
        st.session_state.room_id = 0
        st.session_state.game_started = False
        st.session_state.game_over = False
        st.session_state.win_shown = False
        st.session_state.lose_shown = False
        st.session_state.show_open_door = False
        st.session_state.answer_checked = False
        reset_timer()

#----> starting page  
    if not st.session_state.game_started:
#----> starting page design       
        title_html = '''
        <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 25px; margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
            <div style="font-size: 8em; margin-bottom: 20px;">🗝️</div>
            <h1 style="color: white; font-size: 4.5em; margin-bottom: 15px; font-family: Arial Black, Arial, sans-serif;">ANSWER TO ESCAPE</h1>
            <h2 style="color: #f8f9fa; font-size: 1.8em; margin-bottom: 40px;">🧩 The Ultimate Tech Challenge</h2>
        </div>
        '''
        st.markdown(title_html, unsafe_allow_html=True)
        
#----> game instructions       
        instructions_html = '''
        <div style="background: rgba(255,255,255,0.95); padding: 40px; border-radius: 20px; margin: 30px 0;">
            <h3 style="color: #333; text-align: center; margin-bottom: 35px; font-size: 2.5em;">🎯 How To Play</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 25px; justify-content: center;">
                <div style="background: #e3f2fd; padding: 25px; border-radius: 15px; text-align: center; min-width: 280px;">
                    <div style="font-size: 3em; margin-bottom: 15px;">🏠</div>
                    <h4 style="color: #1976d2; margin-bottom: 12px;">5 Rooms To Escape</h4>
                    <p style="color: #555; margin: 0;">Navigate through 5 challenging tech rooms</p>
                </div>
                <div style="background: #fff3e0; padding: 25px; border-radius: 15px; text-align: center; min-width: 280px;">
                    <div style="font-size: 3em; margin-bottom: 15px;">⏰</div>
                    <h4 style="color: #f57c00; margin-bottom: 12px;">30 Seconds Per Room</h4>
                    <p style="color: #555; margin: 0;">Answer quickly before time runs out!</p>
                </div>
                <div style="background: #f3e5f5; padding: 25px; border-radius: 15px; text-align: center; min-width: 280px;">
                    <div style="font-size: 3em; margin-bottom: 15px;">🧠</div>
                    <h4 style="color: #7b1fa2; margin-bottom: 12px;">Tech Knowledge</h4>
                    <p style="color: #555; margin: 0;">Test your technology expertise</p>
                </div>
            </div>
        </div>
        '''
        st.markdown(instructions_html, unsafe_allow_html=True)
        
#----> start game button        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 PLAY GAME", key="start_game", use_container_width=True, type="primary"):
                st.session_state.game_started = True
                reset_timer()
                st.rerun()
        
        return

#-----> time over check 
    if st.session_state.game_started and not st.session_state.game_over and st.session_state.room_id < TOTAL_ROOMS:
        if time_left() <= 0:
            st.session_state.game_over = True
            st.rerun()

    #------> lose screen
    if st.session_state.game_over:
        if not st.session_state.get("lose_shown", False):
            play_sound_file(SOUNDS / "lose.mp3")
            st.session_state.lose_shown = True

        gameover_html = '''
        <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%); border-radius: 20px; margin: 20px 0;">
            <h1 style="color: white; font-size: 4em; margin-bottom: 20px;">⏰</h1>
            <h1 style="color: white; font-size: 3.5em; margin-bottom: 15px;">GAME OVER!</h1>
            <h2 style="color: #ffcdd2; font-size: 1.5em; margin-bottom: 30px;">🔒 Times Up! You couldnt escape!</h2>
        </div>
        '''
        st.markdown(gameover_html, unsafe_allow_html=True)
        
        stats_html = f'''
        <div style="background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center;">
            <h3 style="color: #333; margin-bottom: 20px; font-size: 2em;">📊 Game Statistics</h3>
            <p style="font-size: 1.4em; color: #555; margin-bottom: 10px;"><strong>Rooms Completed:</strong> {st.session_state.room_id} / {TOTAL_ROOMS}</p>
            <p style="font-size: 1.4em; color: #555;"><strong>Success Rate:</strong> {int((st.session_state.room_id / TOTAL_ROOMS) * 100)}%</p>
        </div>
        '''
        st.markdown(stats_html, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 TRY AGAIN", key="lose_try_again", use_container_width=True, type="primary"):
                reset_game()
                st.rerun()
        with col2:
            if st.button("🚪 QUIT GAME", key="lose_quit", use_container_width=True):
                st.markdown('<div style="text-align: center; padding: 30px;"><h2 style="color: #666;">Thanks for Playing! 👋</h2></div>', unsafe_allow_html=True)
                st.stop()
        return

    #------> winning screen 
    if st.session_state.game_started and st.session_state.room_id >= TOTAL_ROOMS:
        if not st.session_state.get("win_shown", False):
            play_sound_file(SOUNDS / "win.mp3")
            st.balloons()
            st.session_state.win_shown = True

        win_html = '''
        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); border-radius: 20px; margin: 20px 0;">
            <h1 style="color: white; font-size: 4em; margin-bottom: 20px;">🎉</h1>
            <h1 style="color: white; font-size: 3.5em; margin-bottom: 15px;">CONGRATULATIONS!</h1>
            <h2 style="color: #c8e6c9; font-size: 1.5em; margin-bottom: 30px;">🗝️ You successfully escaped all rooms!</h2>
        </div>
        '''
        st.markdown(win_html, unsafe_allow_html=True)
        
        display_door_image("open", TOTAL_ROOMS)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 PLAY AGAIN", key="win_play_again", use_container_width=True, type="primary"):
                reset_game()
                st.rerun()
        with col2:
            if st.button("🚪 QUIT GAME", key="win_quit", use_container_width=True):
                st.stop()
        return

    #-------> showing current room       
    room = RIDDLES[st.session_state.room_id]
    st.title(f"🏠 Room {room['room']} of {TOTAL_ROOMS}")
    
    if st.session_state.get("show_open_door", False):
        display_door_image("open", room['room'])
        st.success("✅ Correct Answer! Door is now open!")
        
        if st.session_state.room_id < TOTAL_ROOMS - 1:
            if st.button(f"🚪 Enter Room {room['room'] + 1}", key="next_room", type="primary"):
                next_room()
                st.rerun()
        else:
            if st.button("🏆 Claim Victory!", key="claim_victory", type="primary"):
                next_room()
                st.rerun()
    else:
        display_door_image("closed", room['room'])
        
        question_html = f'''
        <div style="background: linear-gradient(135deg, #fff3e0, #ffcc80); padding: 25px; border-radius: 15px; margin: 20px 0; border-left: 5px solid #f57c00;">
            <h2 style="color: #e65100; margin-bottom: 15px; text-align: center;">❓ {room["question"]}</h2>
        </div>
        '''
        st.markdown(question_html, unsafe_allow_html=True)
        
        #-------> timer+progress bar    
        current_time_left = time_left()
        deadline_ms = int((st.session_state.start_time + PER_ROOM_SECONDS) * 1000)
        
        timer_html = f'''
        <div style="font-size:20px; font-weight:bold; margin-bottom:10px;" id="countdown">⏳ Time left: {current_time_left} seconds</div>
        <div style="width: 100%; background-color: #ddd; border-radius: 10px; margin-bottom: 20px;">
          <div id="progress-bar" style="height: 20px; width: {(current_time_left/PER_ROOM_SECONDS)*100}%; background-color: {'red' if current_time_left < 10 else 'orange' if current_time_left < 20 else 'green'}; border-radius: 10px; transition: all 0.3s ease;"></div>
        </div>
        <script>
          const target = {deadline_ms};
          const total = {PER_ROOM_SECONDS};
          function tick() {{
            const now = Date.now();
            const left = Math.max(0, Math.floor((target - now) / 1000));
            const pct = Math.max(0, Math.min(100, (left / total) * 100));
            
            const countdown = document.getElementById('countdown');
            const progressBar = document.getElementById('progress-bar');
            
            if (countdown && progressBar) {{
              countdown.innerText = '⏳ Time left: ' + left + ' seconds';
              progressBar.style.width = pct + '%';
              
              if (left <= 5) {{
                progressBar.style.backgroundColor = 'red';
                countdown.style.color = 'red';
              }} else if (left <= 10) {{
                progressBar.style.backgroundColor = 'orange';
                countdown.style.color = 'orange';
              }} else {{
                progressBar.style.backgroundColor = 'green';
                countdown.style.color = 'black';
              }}
            }}

            if (left > 0) {{
              setTimeout(tick, 100);
            }} else {{
              if (countdown) countdown.innerText = '⏰ TIME OVER!';
              if (progressBar) progressBar.style.backgroundColor = 'red';
              setTimeout(function() {{
                window.parent.postMessage({{type: 'streamlit:rerun'}}, '*');
              }}, 100);
            }}
          }}
          tick();
        </script>
        '''
        st.components.v1.html(timer_html, height=80)    
        
#----> progress viewer     
        progress = (st.session_state.room_id / TOTAL_ROOMS)
        st.progress(progress, text=f"Progress: {st.session_state.room_id}/{TOTAL_ROOMS} rooms completed")
        
        #------> answer entry    
        answer = st.text_input("Enter Your Answer:", key=f"answer_{st.session_state.room_id}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 CHECK ANSWER", key="check_answer", type="primary"):
                if current_time_left <= 0:
                    st.session_state.game_over = True
                    st.rerun()
                else:
                    if normalize(answer) in [normalize(a) for a in room["answers"]]:
#-----> sound starter+delay                        
                        st.session_state.answer_checked = True
                        st.session_state.show_open_door = True
                        play_correct_sound_and_proceed(SOUNDS / "correct.mp3")
                        st.success("✅ Correct Answer! Please wait...")
                       
                    else:
                        play_sound_file(SOUNDS / "wrong.mp3")
                        st.error("❌ Wrong Answer! Try again!")
        
        with col2:
            if st.button("🔄 RESTART GAME", key="restart_game"):
                reset_game()
                st.rerun()

if __name__ == "__main__":
    main() 