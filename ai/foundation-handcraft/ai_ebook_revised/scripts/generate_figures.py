from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 900
BG = "#F7FAFC"
NAVY = "#12355B"
BLUE = "#168AAD"
TEAL = "#1A759F"
GREEN = "#52B69A"
PALE = "#EAF4F4"
WHITE = "#FFFFFF"
GRAY = "#526579"
LINE = "#9CB7C5"
ORANGE = "#E09F3E"
RED = "#C8553D"

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


def canvas(title, subtitle=None):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((48, 38, W - 48, H - 38), radius=28, fill=WHITE, outline="#D9E6EC", width=3)
    d.text((90, 75), title, font=font(44, True), fill=NAVY)
    if subtitle:
        d.text((92, 135), subtitle, font=font(24), fill=GRAY)
    return im, d


def centered_text(d, box, text, size=28, color=NAVY, bold=False, spacing=7):
    f = font(size, bold)
    lines = text.split("\n")
    widths = [d.textbbox((0, 0), x, font=f)[2] for x in lines]
    line_h = size + spacing
    total_h = line_h * len(lines) - spacing
    y = (box[1] + box[3] - total_h) / 2
    for line, tw in zip(lines, widths):
        x = (box[0] + box[2] - tw) / 2
        d.text((x, y), line, font=f, fill=color)
        y += line_h


def box(d, xy, label, fill=PALE, outline=BLUE, size=27, bold=True):
    d.rounded_rectangle(xy, radius=24, fill=fill, outline=outline, width=4)
    centered_text(d, xy, label, size=size, color=NAVY, bold=bold)


def arrow(d, start, end, color=BLUE, width=6):
    d.line((start, end), fill=color, width=width)
    import math
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 20
    spread = 0.55
    p1 = (end[0] - length * math.cos(angle - spread), end[1] - length * math.sin(angle - spread))
    p2 = (end[0] - length * math.cos(angle + spread), end[1] - length * math.sin(angle + spread))
    d.polygon((end, p1, p2), fill=color)


def save(im, name):
    im.save(OUT / name, quality=95, dpi=(180, 180))


def ecosystem():
    im, d = canvas("Hệ sinh thái AI", "Từ lĩnh vực rộng đến lớp ứng dụng có thể vận hành")
    boxes = [
        ((90, 235, 390, 410), "AI\nphạm vi tổng quát", NAVY),
        ((480, 215, 780, 390), "Machine Learning\nhọc từ dữ liệu", BLUE),
        ((480, 480, 780, 655), "Hệ luật\ntri thức viết tay", GREEN),
        ((870, 215, 1170, 390), "Deep Learning\nmạng neural nhiều tầng", TEAL),
        ((1260, 215, 1510, 390), "Generative AI\ntạo nội dung", ORANGE),
        ((870, 480, 1170, 655), "Ứng dụng AI\nworkflow + dữ liệu + tool", GREEN),
        ((1260, 480, 1510, 655), "Sản phẩm\nUX + policy + eval", RED),
    ]
    for xy, label, color in boxes:
        box(d, xy, label, fill=WHITE, outline=color, size=25)
    arrow(d, (390, 320), (480, 300), NAVY)
    arrow(d, (390, 340), (480, 560), NAVY)
    arrow(d, (780, 300), (870, 300), BLUE)
    arrow(d, (1170, 300), (1260, 300), TEAL)
    arrow(d, (780, 575), (870, 575), GREEN)
    arrow(d, (1170, 575), (1260, 575), GREEN)
    arrow(d, (1385, 390), (1385, 480), ORANGE)
    d.text((100, 755), "Quy luật chính:", font=font(23, True), fill=NAVY)
    d.text((305, 755), "Model là một thành phần; giá trị và độ an toàn đến từ toàn bộ hệ thống.", font=font(22), fill=GRAY)
    save(im, "01_ai_ecosystem.png")


def token_generation():
    im, d = canvas("LLM tạo câu trả lời theo vòng lặp token", "Mỗi vòng tạo một token rồi cập nhật lại ngữ cảnh")
    y1, y2 = 320, 485
    items = [
        ((95, y1, 330, y2), "Văn bản\nđầu vào", NAVY),
        ((410, y1, 645, y2), "Tokenizer\nToken ID", BLUE),
        ((725, y1, 960, y2), "Transformer\nphân phối", TEAL),
        ((1040, y1, 1275, y2), "Sampling\nchọn token", ORANGE),
        ((1355, y1, 1510, y2), "Token\nmới", GREEN),
    ]
    for xy, label, c in items:
        box(d, xy, label, fill=WHITE, outline=c, size=25)
    for a, b in [((330, 403), (410, 403)), ((645, 403), (725, 403)), ((960, 403), (1040, 403)), ((1275, 403), (1355, 403))]:
        arrow(d, a, b)
    d.arc((650, 465, 1480, 760), start=5, end=190, fill=GREEN, width=7)
    arrow(d, (657, 612), (650, 570), GREEN)
    d.text((795, 650), "Ghép token mới vào chuỗi và lặp", font=font(28, True), fill=GREEN)
    d.text((125, 720), "Điểm kiểm soát", font=font(22, True), fill=NAVY)
    d.text((390, 720), "context", font=font(22, True), fill=NAVY)
    d.text((600, 720), "model", font=font(22, True), fill=TEAL)
    d.text((775, 720), "temperature / top-p", font=font(22, True), fill=ORANGE)
    d.text((1150, 720), "điều kiện dừng", font=font(22, True), fill=GREEN)
    save(im, "02_token_generation.png")


def rag():
    im, d = canvas("RAG: truy xuất trước, tạo sinh sau", "Tách rõ luồng chuẩn bị dữ liệu và luồng trả lời")
    d.text((105, 205), "LẬP CHỈ MỤC", font=font(25, True), fill=NAVY)
    d.text((105, 535), "TRUY VẤN", font=font(25, True), fill=NAVY)
    top = [
        ((270, 185, 500, 320), "Tài liệu", NAVY),
        ((590, 185, 820, 320), "Làm sạch\n+ chunk", BLUE),
        ((910, 185, 1140, 320), "Embedding\n+ metadata", TEAL),
        ((1230, 185, 1490, 320), "Search index\nVector store", GREEN),
    ]
    bottom = [
        ((270, 515, 500, 650), "Câu hỏi", NAVY),
        ((590, 515, 820, 650), "Retrieval\n+ rerank", BLUE),
        ((910, 515, 1140, 650), "Context\ncó nguồn", TEAL),
        ((1230, 515, 1490, 650), "LLM trả lời\n+ citation", ORANGE),
    ]
    for xy, label, c in top + bottom:
        box(d, xy, label, fill=WHITE, outline=c, size=23)
    for row in (top, bottom):
        for i in range(len(row)-1):
            arrow(d, (row[i][0][2], (row[i][0][1]+row[i][0][3])//2), (row[i+1][0][0], (row[i+1][0][1]+row[i+1][0][3])//2))
    arrow(d, (1360, 320), (800, 515), GREEN)
    d.text((875, 390), "tìm trong index", font=font(23, True), fill=GREEN)
    d.rounded_rectangle((250, 735, 1500, 815), radius=20, fill=PALE)
    centered_text(d, (250, 735, 1500, 815), "RAG giảm thiếu dữ kiện; evaluation vẫn phải kiểm tra retrieval và câu trả lời.", 24, NAVY, True)
    save(im, "03_rag_pipeline.png")


def workflow_agent():
    im, d = canvas("Workflow và Agent khác nhau ở quyền lựa chọn", "Cả hai đều cần runtime, state, giới hạn và quan sát")
    d.text((105, 210), "WORKFLOW", font=font(26, True), fill=NAVY)
    wf = [((110, 270, 330, 415), "Input", NAVY), ((430, 270, 650, 415), "Bước A", BLUE), ((750, 270, 970, 415), "Điều kiện", TEAL), ((1070, 270, 1290, 415), "Bước B", GREEN), ((1370, 270, 1510, 415), "Kết quả", NAVY)]
    for xy, label, c in wf: box(d, xy, label, WHITE, c, 24)
    for i in range(len(wf)-1): arrow(d, (wf[i][0][2], 342), (wf[i+1][0][0], 342))
    d.text((105, 525), "AGENT", font=font(26, True), fill=NAVY)
    box(d, (110, 590, 380, 750), "Mục tiêu\n+ state", WHITE, NAVY, 24)
    box(d, (580, 555, 900, 785), "Model quyết định\nbước tiếp theo", WHITE, ORANGE, 25)
    tools = [((1110, 520, 1390, 625), "Tool: tìm kiếm", BLUE), ((1110, 660, 1390, 765), "Tool: hành động", RED)]
    for xy, label, c in tools: box(d, xy, label, WHITE, c, 22)
    arrow(d, (380, 670), (580, 670))
    arrow(d, (900, 625), (1110, 575), ORANGE)
    arrow(d, (900, 700), (1110, 712), ORANGE)
    arrow(d, (1110, 600), (900, 610), GREEN)
    d.text((550, 825), "Agent: đường đi động, nhưng quyền và điều kiện dừng phải tĩnh.", font=font(24, True), fill=GRAY)
    save(im, "04_workflow_agent.png")


def architecture():
    im, d = canvas("Kiến trúc tham chiếu cho ứng dụng AI", "Ranh giới trách nhiệm quan trọng hơn số lượng dịch vụ")
    layers = [
        ((170, 195, 1430, 300), "TRẢI NGHIỆM  •  UI  •  API  •  AUTH", NAVY),
        ((170, 335, 1430, 440), "ĐIỀU PHỐI  •  WORKFLOW  •  AGENT RUNTIME  •  STATE", BLUE),
        ((170, 475, 1430, 580), "CONTEXT  •  PROMPT  •  RETRIEVAL  •  MEMORY  •  PERMISSION", TEAL),
        ((170, 615, 1430, 720), "MODEL GATEWAY  •  TOOL GATEWAY  •  HỆ THỐNG NGHIỆP VỤ", GREEN),
    ]
    for xy, label, c in layers:
        box(d, xy, label, fill=WHITE, outline=c, size=24)
    for i in range(len(layers)-1):
        arrow(d, (800, layers[i][0][3]), (800, layers[i+1][0][1]), LINE, 5)
    d.rounded_rectangle((95, 175, 155, 740), radius=20, fill=ORANGE)
    d.text((105, 330), "T\nR\nU\nS\nT", font=font(22, True), fill=WHITE, spacing=15)
    d.text((150, 770), "Evaluation • Guardrail • Audit • Observability • Human approval", font=font(24, True), fill=ORANGE)
    save(im, "05_reference_architecture.png")


def evaluation():
    im, d = canvas("Vòng đời đánh giá và cải tiến", "Mỗi lỗi đã xác minh trở thành dữ liệu ngăn regression")
    nodes = [
        ((630, 185, 970, 310), "Ca sử dụng\n+ tiêu chí", NAVY),
        ((1080, 350, 1420, 475), "Chạy hệ thống\n+ thu trace", BLUE),
        ((970, 625, 1310, 750), "Chấm điểm\n+ phân loại lỗi", ORANGE),
        ((290, 625, 630, 750), "Sửa đúng lớp\nmodel/context/tool", GREEN),
        ((180, 350, 520, 475), "Regression\n+ release gate", TEAL),
    ]
    for xy, label, c in nodes: box(d, xy, label, WHITE, c, 24)
    centers = [((800, 310), (1080, 400)), ((1250, 475), (1170, 625)), ((970, 690), (630, 690)), ((460, 625), (350, 475)), ((520, 400), (650, 270))]
    for a,b in centers: arrow(d,a,b)
    d.ellipse((650, 390, 950, 590), fill=PALE, outline=NAVY, width=5)
    centered_text(d, (650, 390, 950, 590), "Evaluation set\nlà tài sản\ncủa sản phẩm", 28, NAVY, True)
    save(im, "06_evaluation_loop.png")


if __name__ == "__main__":
    ecosystem()
    token_generation()
    rag()
    workflow_agent()
    architecture()
    evaluation()
    print(f"Generated figures in {OUT}")
