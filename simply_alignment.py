import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
# 第三版，重写算法，极大降低时间复杂度，加入输入判断，并改善结果显示

def check_string(input_list):  
    # 允许的字符集合（不区分大小写）  
    allowed_chars = set('AGCTUagctu')  
    
    for item in input_list:
        cleaned_item = item.strip() 
        if all(char in allowed_chars for char in cleaned_item): 
            return True
        else:
            return False


def global_alignment(seq1, seq2, match_score=0, mismatch_score=1, gap_penalty=1):  
    m, n = len(seq1), len(seq2)  
    score_matrix = [[0] * (n + 1) for _ in range(m + 1)]  
      
    # 初始化第一行和第一列  
    for i in range(1, m + 1):  
        score_matrix[i][0] = score_matrix[i-1][0] + gap_penalty  
    for j in range(1, n + 1):  
        score_matrix[0][j] = score_matrix[0][j-1] + gap_penalty  
          
    # 填充得分矩阵  
    for i in range(1, m + 1):  
        for j in range(1, n + 1):  
            match = score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_score)  
            delete = score_matrix[i-1][j] + gap_penalty  
            insert = score_matrix[i][j-1] + gap_penalty  
            score_matrix[i][j] = min(match, delete, insert)  
    return score_matrix

def find_seq_distance(seq1,seq2,max_distance,min_length):
    out = []
    for i in range(len(seq1) - min_length + 1):
        for j in range(len(seq2) - min_length + 1):
            subseq1 = seq1[i:]
            subseq2 = seq2[j:]
            score_matrix = global_alignment(subseq1,subseq2)
            for k in range(min_length+1,len(score_matrix)): 
                for l in range(min_length+1,len(score_matrix[k])): 
                    if score_matrix[k][l] <= max_distance:
                        out.append((subseq1[:k], subseq2[:l]))
    return(out)

def on_submit():
    strings = [line for line in input_str1.get("1.0", tk.END).split("\n") if line]
    distance_dict = {}  # 定义字典来存结果

    try:
        if check_string(strings) == True:
            for string in strings:
                distance_dict[string] = []
            
            for i in range(len(strings)):
                for j in range(i+1, len(strings)):
                    similarity = find_seq_distance(strings[i], strings[j], max_distance=int(threshold.get()), min_length=int(min_length.get()))
                    if similarity:
                        distance_dict[strings[i]].append((strings[j], similarity))
                        distance_dict[strings[j]].append((strings[i], similarity))

            # 创建一个字符串来显示所有的编辑距离 
            info_str = ""
            count = 0
            for key, value in distance_dict.items():
                count += 1
                if value:
                    info_str += f"{count}.{key}:\n这段序列的相似序列有:\n" + ", ".join([v[0] for v in value]) + "\n\n"
                    for item in value:
                        info_str += f"对于序列{item[0]}, 相似序列如下:\n"
                        for subseq_info in item[1]:
                            info_str += f"{subseq_info}\n"
                    info_str += "\n--------------------------------------\n"
                else:
                    info_str += f"{count}. {key} \n没有找到以上序列的相似序列。\n\n"

            result = tk.Tk()
            result.title("比对结果")

            text_box = scrolledtext.ScrolledText(result)
            text_box.pack(fill="both", expand=True)
            text_box.insert(tk.END, info_str)
        else:
            messagebox.showinfo("输入错误","输入只能为AGCTU（不分大小写）")
    except Exception as e:
        messagebox.showerror("错误", str(e))

# GUI制作
root = tk.Tk()    
root.title("相似序列查找器")    

# 第一个输入框的标题  
label1 = tk.Label(root, text="输入序列，每行一个序列，并以回车隔开:")  
label1.pack()

input_str1 = tk.Text(root, width=50, height=25)    
input_str1.pack()    
    
# 第二个输入框的标题  
label2 = tk.Label(root, text="差异上限（插入、删除、替换之和）:")  
label2.pack() 
# 定义阈值  
threshold = tk.Entry(root, width=5) 
threshold.pack()

# 第三个输入框的标题
label3 = tk.Label(root,text="最小比对长度（>）：")
label3.pack()
# 定义比对长度
min_length = tk.Entry(root, width=5)
min_length.pack()

submit_button = tk.Button(root, text="查询", command=on_submit)    
submit_button.pack()    
    
root.mainloop()
