import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
import pandas as pd
import os
from PIL import Image, ImageTk, ImageOps
import datetime # [추가] 내역에 날짜 기록용

# 파일 경로 설정
CSV_FILE = "books.csv"      # 전체 게시글 저장
MATCH_FILE = "matches.csv"  # 성사된 매칭 내역 저장

COLUMNS = ['title', 'nickname', 'contact', 'my_book', 'my_img', 'want_book', 'want_img']
MATCH_COLUMNS = ['date', 'my_nick', 'my_book', 'partner_nick', 'partner_book', 'partner_contact']

BOOK_LIST = [
    "JAVA 프로그래밍",
    "심화 프로그래밍",
    "C 프로그래밍",
    "데이터베이스",
    "운영체제",
    "컴퓨터 네트워크",
    "소프트웨어 공학",
    "웹 프로그래밍",
    "알고리즘",
    "자료구조",
    "컴퓨터 구조",
    "정보보안 개론",
    "이산수학",
    "모바일 앱 프로그래밍",
    "지능웹설계",
]




# 데이터 관리 로직 (게시글 & 매칭 내역)
# ==========================================

def read_csv_safe(file_path, cols):
    if not os.path.exists(file_path):
        return pd.DataFrame() 

    try:
        df = pd.read_csv(file_path)
        # 컬럼 검사 (파일이 꼬였는지 확인)
        if not all(col in df.columns for col in cols):
            raise ValueError("파일 형식 불일치")
        return df
    except Exception as e:
        print(f"{file_path} 오류 감지({e}): 초기화 진행")
        if os.path.exists(file_path):
            os.remove(file_path)
        return pd.DataFrame()

def save_to_csv(title, nickname, contact, my_book, my_img, want_book, want_img):
    new_data = {
        'title': [title], 'nickname': [nickname], 'contact': [contact],
        'my_book': [my_book], 'my_img': [my_img],
        'want_book': [want_book], 'want_img': [want_img]
    }
    new_df = pd.DataFrame(new_data, columns=COLUMNS)

    if os.path.exists(CSV_FILE):
        new_df.to_csv(CSV_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        new_df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')

# 매칭 성공 내역 저장 함수
def save_match_record(my_nick, my_book, partner_nick, partner_book, partner_contact):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") # 현재 시간
    
    new_data = {
        'date': [now],
        'my_nick': [my_nick],
        'my_book': [my_book],
        'partner_nick': [partner_nick],
        'partner_book': [partner_book],
        'partner_contact': [partner_contact]
    }
    new_df = pd.DataFrame(new_data, columns=MATCH_COLUMNS)

    if os.path.exists(MATCH_FILE):
        new_df.to_csv(MATCH_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        new_df.to_csv(MATCH_FILE, index=False, encoding='utf-8-sig')

def check_match(my_give, my_take):
    df = read_csv_safe(CSV_FILE, COLUMNS)
    if df.empty: return None

    try:
        user_give = str(my_give).strip()
        user_take = str(my_take).strip()

        for index, row in df.iterrows():
            target_give = str(row['my_book']).strip()
            target_want = str(row['want_book']).strip()

            if target_give == user_take and target_want == user_give:
                # 매칭된 상대방의 모든 정보를 반환 (닉네임, 연락처, 책이름)
                return row
    except:
        pass
    return None





# 게시글 상세 보기
# ==========================================

def load_image(path, size):
    try:
        if not path or not os.path.exists(path): raise Exception
        img = Image.open(path)
        try: img = ImageOps.exif_transpose(img)
        except: pass
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except:
        img = Image.new('RGB', size, color='#F0F0F0')
        return ImageTk.PhotoImage(img)

def open_detail_window(row):
    detail = Toplevel(window)
    detail.title("게시글 상세 정보")
    detail.geometry("500x700")
    detail.configure(bg="white")

    tk.Label(detail, text=row['title'], font=("Arial", 18, "bold"), bg="white", wraplength=450).pack(pady=(30, 10))
    tk.Label(detail, text=f"작성자: {row['nickname']}", font=("Arial", 12), fg="#666", bg="white").pack()
    tk.Frame(detail, height=1, bg="#E0E0E0").pack(fill="x", pady=20)

    img_frame = tk.Frame(detail, bg="white")
    img_frame.pack()
    BIG_SIZE = (180, 180)
    
    tk.Label(img_frame, text="보유한 책", font=("Arial", 10, "bold"), bg="white", fg="#007AFF").grid(row=0, column=0)
    img1 = load_image(row['my_img'], BIG_SIZE)
    lbl1 = tk.Label(img_frame, image=img1, bg="white"); lbl1.image = img1
    lbl1.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(img_frame, text=row['my_book'], font=("Arial", 11), bg="white").grid(row=2, column=0)

    tk.Label(img_frame, text="↔", font=("Arial", 20), bg="white", fg="#999").grid(row=1, column=1)

    tk.Label(img_frame, text="원하는 책", font=("Arial", 10, "bold"), bg="white", fg="#E65100").grid(row=0, column=2)
    img2 = load_image(row['want_img'], BIG_SIZE)
    lbl2 = tk.Label(img_frame, image=img2, bg="white"); lbl2.image = img2
    lbl2.grid(row=1, column=2, padx=10, pady=5)
    tk.Label(img_frame, text=row['want_book'], font=("Arial", 11), bg="white").grid(row=2, column=2)

    tk.Frame(detail, height=1, bg="#E0E0E0").pack(fill="x", pady=20)

    tk.Button(detail, text="닫기", bg="#E0E0E0", fg="black", font=("Arial", 12, "bold"), 
              relief="flat", command=detail.destroy).pack(side="bottom", pady=40, ipadx=40, ipady=5)


def create_card(parent, row):
    card = tk.Frame(parent, bg="white", highlightbackground="#E0E0E0", highlightthickness=1, cursor="hand2")
    card.pack(fill="x", padx=20, pady=10)
    
    def on_click(event): open_detail_window(row)
    card.bind("<Button-1>", on_click)

    inner = tk.Frame(card, bg="white", padx=15, pady=15)
    inner.pack(fill="both", expand=True)
    inner.bind("<Button-1>", on_click)

    img_frame = tk.Frame(inner, bg="white")
    img_frame.pack(side="left")
    img_frame.bind("<Button-1>", on_click)
    
    IMG_SIZE = (80, 80)
    img1 = load_image(row['my_img'], IMG_SIZE)
    lbl1 = tk.Label(img_frame, image=img1, bg="white"); lbl1.image = img1
    lbl1.pack(side="left"); lbl1.bind("<Button-1>", on_click)
    
    lbl_arrow = tk.Label(img_frame, text="▶", font=("Arial", 16), fg="#CCCCCC", bg="white")
    lbl_arrow.pack(side="left", padx=15); lbl_arrow.bind("<Button-1>", on_click)
    
    img2 = load_image(row['want_img'], IMG_SIZE)
    lbl2 = tk.Label(img_frame, image=img2, bg="white"); lbl2.image = img2
    lbl2.pack(side="left"); lbl2.bind("<Button-1>", on_click)

    text_frame = tk.Frame(inner, bg="white", padx=25)
    text_frame.pack(side="left", fill="both", expand=True); text_frame.bind("<Button-1>", on_click)
    
    lbl_title = tk.Label(text_frame, text=row['title'], font=("Arial", 16, "bold"), bg="white", anchor="w")
    lbl_title.pack(fill="x"); lbl_title.bind("<Button-1>", on_click)
    
    trade = f"보유: {row['my_book']}  ↔  희망: {row['want_book']}"
    lbl_trade = tk.Label(text_frame, text=trade, font=("Arial", 13), fg="#007AFF", bg="white", anchor="w")
    lbl_trade.pack(fill="x", pady=(8,0)); lbl_trade.bind("<Button-1>", on_click)
    
    lbl_nick = tk.Label(text_frame, text=f"작성자: {row['nickname']}", font=("Arial", 11), fg="#888", bg="white", anchor="w")
    lbl_nick.pack(fill="x", pady=(8,0)); lbl_nick.bind("<Button-1>", on_click)



def refresh_board():
    for widget in scrollable_frame.winfo_children(): widget.destroy()
    df = read_csv_safe(CSV_FILE, COLUMNS)
    if df.empty:
        tk.Label(scrollable_frame, text="아직 등록된 교환 글이 없습니다.", bg="white", fg="#999").pack(pady=50)
        return
    try:
        for idx, row in df.iloc[::-1].iterrows(): create_card(scrollable_frame, row)
    except: pass






# 교환 매칭 내역 버튼 설정
# ==========================================

def open_history_window():
    history = Toplevel(window)
    history.title("교환 성사 내역")
    history.geometry("500x600")

    # 창 라벨
    tk.Label(history, text="교환 성사 내역", font=("Arial", 18, "bold"), bg="#F9F9F9", fg="#333").pack(pady=20)

    # 내역 리스트 영역
    hist_frame = tk.Frame(history, bg="#F9F9F9")
    hist_frame.pack(fill="both", expand=True, padx=10)
    df = read_csv_safe(MATCH_FILE, MATCH_COLUMNS)
    if df.empty:
        tk.Label(hist_frame, text="아직 성사된 거래가 없습니다.", bg="#F9F9F9", fg="#999").pack(pady=50)
        return

    # 최신 내역이 위로 오게 해줌
    for idx, row in df.iloc[::-1].iterrows():

        # 카드 디자인
        card = tk.Frame(hist_frame, bg="white",highlightbackground="#E0E0E0", highlightthickness=1, bd=0, relief="flat")
        card.pack(fill="x", padx=10, pady=10)
        
        # 날짜 표기
        tk.Label(card, text=f"성사 일시: {row['date']}", font=("Arial", 9), fg="#888", bg="#F5F5F5", anchor="w", padx=10).pack(fill="x", ipady=3)
        
        # 내용
        content = tk.Frame(card, bg="white", padx=15, pady=15)
        content.pack(fill="x")
        
        info_text = f"나의 [{row['my_book']}] ↔ 상대방 [{row['partner_book']}]"
        tk.Label(content, text=info_text, font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        tk.Label(content, text=f"상대방 닉네임: {row['partner_nick']}", font=("Arial", 10), bg="white").pack(anchor="w", pady=(5,0))
        
        # [핵심] 연락처 강조
        contact_box = tk.Frame(content, bg="#FFFFFF", padx=10, pady=5) 
        contact_box.pack(fill="x", pady=(10,0))
        tk.Label(contact_box, text=f"상대방 연락처: {row['partner_contact']}", font=("Arial", 12, "bold"), fg="#007AFF", bg="#E3F2FD").pack()





# ==========================================
# 등록 및 메인 UI 설정
# ==========================================

def open_register_window():
    top = Toplevel(window)
    top.title("교환 글 등록")
    top.geometry("400x650")
    top.configure(bg="white")
    
    my_img_path = tk.StringVar(); want_img_path = tk.StringVar()

    def find_img(var, btn):
        f = filedialog.askopenfilename(parent=top, filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")]) # 사진 파일 확장자 중에서만 고르게 함
        if f: var.set(f); btn.config(text="선택 완료", fg="black")

    # 정보 입력 전부 안했을 시
    def save():
        if not entry_title.get() or not entry_nick.get() or not combo_give.get() or not combo_take.get():
            messagebox.showwarning("오류", "정보를 모두 입력해주세요."); return

        # 게시글 csv에 저장
        save_to_csv(entry_title.get(), entry_nick.get(), entry_contact.get(),
                    combo_give.get(), my_img_path.get(), combo_take.get(), want_img_path.get())
        
        # 매칭 확인
        partner_row = check_match(combo_give.get(), combo_take.get())
        
        if partner_row is not None:
            p_nick = partner_row['nickname']
            p_contact = partner_row['contact']
            p_book = partner_row['my_book'] # 상대방이 가진 책
            
            # 매칭 내역을 파일에 저장
            save_match_record(entry_nick.get(), combo_give.get(), p_nick, p_book, p_contact)

            messagebox.showinfo("매칭 성공!", f"교환 상대를 찾았습니다.\n내역 메뉴에서 연락처를 확인하세요.") # 매칭 됐을때 성공 알림
        else:
            messagebox.showinfo("등록 완료", "게시글이 등록되었습니다.") # 매칭 안됬으면 그냥 게시글 등록

        refresh_board()
        top.destroy()


    # 기본 정보 입력란

    content_frame = tk.Frame(top, bg="white", padx=20, pady=20)
    content_frame.pack(fill="both", expand=True)

    def add_lbl(txt): tk.Label(content_frame, text=txt, bg="white", font=("Arial", 9,"bold")).pack(anchor="w", pady=(15,5))
    
    add_lbl("게시글 제목")
    entry_title = tk.Entry(content_frame, relief="solid", bd=1); entry_title.pack(fill="x", ipady=5)
    
    add_lbl("닉네임"); entry_nick = tk.Entry(content_frame, relief="solid", bd=1); entry_nick.pack(fill="x", ipady=5)
    add_lbl("연락처"); entry_contact = tk.Entry(content_frame, relief="solid", bd=1); entry_contact.pack(fill="x", ipady=5)

    tk.Frame(content_frame, height=1, bg="#E0E0E0").pack(fill="x", pady=20) # 하단 구분선
    
    # 교환 정보 및 이미지 등록

    add_lbl("나의 책 (줄 책)")
    combo_give = ttk.Combobox(content_frame, values=BOOK_LIST, state="readonly"); combo_give.pack(fill="x", ipady=5) # 줄 책 콤보박스
    btn_give = tk.Button(content_frame, text="사진 첨부", bg="white", fg="black", relief="solid", bd=1, command=lambda: find_img(my_img_path, btn_give))
    btn_give.pack(fill="x", pady=5)

    add_lbl("원하는 책 (받을 책)")
    combo_take = ttk.Combobox(content_frame, values=BOOK_LIST, state="readonly"); combo_take.pack(fill="x", ipady=5) # 받을 책 콤보박스
    btn_take = tk.Button(content_frame, text="사진 첨부", bg="white", fg="black", relief="solid", bd=1, command=lambda: find_img(want_img_path, btn_take))
    btn_take.pack(fill="x", pady=5)

    tk.Button(content_frame, text="등록 완료", bg="#E0E0E0", fg="black", height=2, relief="flat", command=save).pack(fill="x", pady=30)


# 메인 실행
window = tk.Tk()
window.title("끼리 - 교내 전공도서 교환") # 메인 타이틀
window.geometry("1000x600") # 메인 페이지 크기

# 로고 이미지 영역
header = tk.Frame(window, bg="white", pady=20); header.pack(fill="x") #로고 이미지 불러옴
logo = ImageTk.PhotoImage(Image.open("logo.png").resize((100,40)))
tk.Label(header, image=logo, bg="white").pack()

# 로고 아래 가로 선 생성
tk.Frame(window, height=1, bg="#E0E0E0").pack(fill="x")

# 하단 버튼 영역
bot_frame = tk.Frame(window, bg="white", pady=20); bot_frame.pack(side="bottom", fill="x")

# 내역 버튼
btn_hist = tk.Button(bot_frame, text="교환 성사 내역", bg="#F5F5F5", fg="black", relief="flat", command=open_history_window)
btn_hist.pack(side="left", padx=20, ipadx=10, ipady=10)

# 등록 버튼 
btn_add = tk.Button(bot_frame, text="+ 교환 글 쓰기", bg="#F5F5F5", fg="black", relief="flat", command=open_register_window)
btn_add.pack(side="right", padx=20, ipadx=40, ipady=15)

# 게시글 리스트 영역
scrollable_frame = tk.Frame(window, bg="white")
scrollable_frame.pack(fill="both", expand=True)

refresh_board()
window.mainloop()