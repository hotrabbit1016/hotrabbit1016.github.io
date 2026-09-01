"""Generate the public Chinese and English resume PDFs.

Run with Python plus reportlab and pypdf. Outputs:
  resume/resume.pdf
  resume/resume-en.pdf
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "resume"
TEMP_DIR = ROOT / "tmp" / "pdfs"

ACCENT = colors.HexColor("#234A6D")
INK = colors.HexColor("#17202A")
SOFT = colors.HexColor("#52606D")
LINE = colors.HexColor("#D9E0E6")


RESUMES = {
    "zh": {
        "output": OUTPUT_DIR / "resume.pdf",
        "lang": "zh-Hant",
        "title": "履歷 - 吳承儒 後端工程師",
        "name": "吳承儒  Jack Wu",
        "role": "後端工程師 / Backend Engineer",
        "summary_title": "專業摘要",
        "summary": (
            "5 年後端開發經驗，專注於線上娛樂平台。主力為 C#/.NET，並使用 Go 建置稽核資料管道、"
            "以 Python 開發實體賽道控制與 AI 影像判定。工作橫跨交易與即時推播、分散式協調、硬體控制和電腦視覺。"
            "習慣優先處理失效路徑，包括重複或遺失的訊號、延遲、競態條件、AI 誤判與設備故障。"
        ),
        "experience_title": "工作經歷",
        "experience": [
            {
                "heading": "泰鑫軟體 | 後端工程師 | 2024/01 - 現在",
                "bullets": [
                    "原團隊與產品線在經營者更換後一同移轉；負責桌台客戶端重構、營運後台、聊天平台操作稽核，以及實體賽道控制與 AI 賽果判定。",
                    "以 .NET、Go 與 Python 開發正式環境服務，涵蓋多 Pod 協調、非同步稽核資料管道、硬體抽象層與即時影像推論。",
                    "約一年跨國遠端帶領一名菲律賓工程師，負責需求拆解、技術方向討論、程式碼審查與開發進度追蹤。",
                ],
            },
            {
                "heading": "凱馺國際、鼎順數位科技 | 後端工程師 | 2021/04 - 2023/12",
                "bullets": [
                    "兩間公司由同一經營者與團隊運作，工作連續未中斷；從桌台報表轉檔與狀態處理，逐步負責玩家下注、取消下注與結算服務。",
                    "以交易流程確保下注一致性，結算完成後透過 SignalR 即時推播；跨服務狀態變更使用 RabbitMQ 事件處理。正式服務前後維護約四年。",
                    "開發現場 WPF 桌台操作端；其中一代主畫面與核心邏輯九成以上由我實作，並加入二次確認、錯誤分層與完整狀態記錄。",
                ],
            },
        ],
        "skills_title": "技術能力",
        "skills": [
            ("後端", "C# / .NET 10、ASP.NET Core、EF Core、Go（Gin、Ent、Uber Fx）、Python"),
            ("即時與訊息", "SignalR、WebSocket、RabbitMQ、Redis Streams"),
            ("資料儲存", "MySQL、Redis（Lua、分散式鎖）、ClickHouse、Elasticsearch"),
            ("部署與維運", "Docker、Kubernetes、Helm、GitLab CI、ArgoCD、OpenTelemetry"),
            ("AI 與影像", "YOLO、Roboflow、PyTorch、TensorFlow、OpenCV、ONNX"),
            ("硬體介接", "SPI（MCP23S17）、UART / RF、Raspberry Pi、基礎焊接與電路板設計討論"),
        ],
        "education_title": "學歷與語言",
        "education": "國立中興大學 電機工程學系 | 中文（母語） | 英文（TOEIC 770）",
        "projects_title": "代表專案",
        "projects": [
            {
                "heading": "桌台客戶端重構 | 2025 - 2026",
                "stack": ".NET 10 | Redis | Kubernetes | xUnit",
                "bullets": [
                    "將只能在單機執行的 WPF 程式重構為可多 Pod 部署的服務；主程式與測試由我獨立設計實作。",
                    "使用 Redis + Lua 實作桌台租約，原子化 acquire、renew、release，避免兩個 Pod 同時接管同一張桌而重複處理訊號。",
                    "採 Supervisor-Worker、一桌一個 DI scope；續租失敗立即停止 worker。以 State Pattern 與 TimeProvider 測試八種桌台狀態和調度核心。",
                    "移除版控中的明文密碼與連線字串，改由 Kubernetes Secret 在部署時注入。",
                ],
            },
            {
                "heading": "聊天平台操作稽核 | 2026",
                "stack": "Go | Gin | Redis Streams | ClickHouse | Uber Fx",
                "bullets": [
                    "從方案評估、設計文件到上線獨立完成，讓稽核與客服可查詢誰在何時修改了什麼。",
                    "主請求將紀錄送入 Redis Stream，由 Consumer Group 非同步寫入 ClickHouse；避免稽核拖慢操作，並以分區和 TTL 管理資料。",
                    "分別在 Middleware 與 Service 蒐集 HTTP 語意及前後狀態，最後匯流；將 ID 與 enum 轉成稽核人員可直接理解的名稱。",
                    "將查詢條件做成封閉型別並共用驗證邏輯，無效值直接回 400；時區界線保留寬鬆後端防線，精準限制由前端負責。",
                ],
            },
            {
                "heading": "實體賽道控制與韌體 | 2024 - 2026",
                "stack": "Python | SPI | UART / RF | Raspberry Pi | Flask | OpenTelemetry",
                "bullets": [
                    "獨立開發 8 條實體彈珠賽道的控制軟體與監控介面，涵蓋感測器、閘門、賽事流程與 OBS 直播畫面切換。",
                    "透過 SPI 驅動 MCP23S17，讀取最多 28 路光學感測器，並自動辨識兩代感測板；無硬體時可退回模擬模式。",
                    "針對會遺失的 RF 訊號設計重試、重新初始化、連線檢查與資源釋放等多層復原機制，使設備異常後可自行恢復。",
                    "以 Strategy + Factory 隔離八條賽道的不同流程，三支程式由 systemd 分別常駐，監控介面失效不會中斷賽道控制。",
                ],
            },
            {
                "heading": "彈珠賽事影像判定 | 2024 - 2026",
                "stack": "Python | YOLO | Roboflow | PyTorch | OpenCV | ONNX | FastAPI",
                "bullets": [
                    "獨立完成模型訓練、判定邏輯、查詢 API 與現場介面；系統已上線並取代人工影像判讀。",
                    "把每顆球訓練成獨立 class，避開多物件追蹤的 ID switch；以四狀態機處理落球判定。",
                    "所有門檻使用時間而非 frame 數，透過二段確認、存活門檻與 stale 清理分別吸收漏偵測、誤判和 ghost track。",
                    "排名採最後偵測時間而非確認落球時間，避免確認延遲影響公平性；推論放在獨立 thread，保持現場介面可操作。",
                ],
            },
        ],
        "footer": "吳承儒 | 後端工程師",
    },
    "en": {
        "output": OUTPUT_DIR / "resume-en.pdf",
        "lang": "en-US",
        "title": "Resume - Jack Wu, Backend Engineer",
        "name": "Jack Wu",
        "role": "Backend Engineer | Wu Cheng-Ju",
        "summary_title": "PROFESSIONAL SUMMARY",
        "summary": (
            "Backend Engineer with five years of experience building production systems for online entertainment platforms. "
            "Primary stack: C#/.NET, with Go for audit data pipelines and Python for physical track control and computer vision. "
            "Work spans transaction services, real-time delivery, distributed coordination, hardware integration, and AI inference. "
            "I design for failure paths such as duplicate or missing signals, latency, race conditions, unreliable inference, and device faults."
        ),
        "experience_title": "EXPERIENCE",
        "experience": [
            {
                "heading": "Sentinel IT | Backend Engineer | Jan 2024 - Present",
                "bullets": [
                    "Moved with the original team and product line after a change of ownership. Own work across the table-client rewrite, operations back-office, chat-platform audit logging, physical track control, and AI result judging.",
                    "Built production services in .NET, Go, and Python, covering multi-pod coordination, asynchronous audit pipelines, hardware abstraction, and real-time computer vision.",
                    "Remotely led one developer based in the Philippines for about a year, covering requirement breakdown, technical direction, code review, and delivery tracking.",
                ],
            },
            {
                "heading": "Ifalo International / Dingshun Digital | Backend Engineer | Apr 2021 - Dec 2023",
                "bullets": [
                    "Worked continuously with the same owner, team, and product line across two companies. Progressed from report conversion and table-state handling to player betting, cancellation, and settlement services.",
                    "Implemented transactional betting flows, pushed settlement results over SignalR, and used RabbitMQ events for cross-service state changes. Maintained the production service for about four years.",
                    "Developed the on-site WPF table console; wrote more than 90% of one generation's main view and core logic, including double confirmation, layered error handling, and full-state diagnostics.",
                ],
            },
        ],
        "skills_title": "TECHNICAL SKILLS",
        "skills": [
            ("Backend", "C# / .NET 10, ASP.NET Core, EF Core, Go (Gin, Ent, Uber Fx), Python"),
            ("Realtime & Messaging", "SignalR, WebSocket, RabbitMQ, Redis Streams"),
            ("Data Stores", "MySQL, Redis (Lua, distributed locks), ClickHouse, Elasticsearch"),
            ("Infrastructure", "Docker, Kubernetes, Helm, GitLab CI, ArgoCD, OpenTelemetry"),
            ("AI & Vision", "YOLO, Roboflow, PyTorch, TensorFlow, OpenCV, ONNX"),
            ("Hardware", "SPI (MCP23S17), UART / RF, Raspberry Pi, basic soldering and PCB design discussions"),
        ],
        "education_title": "EDUCATION & LANGUAGES",
        "education": "National Chung Hsing University, B.S. in Electrical Engineering | Mandarin (native) | English (TOEIC 770)",
        "projects_title": "SELECTED PROJECTS",
        "projects": [
            {
                "heading": "Table Client Rewrite | 2025 - 2026",
                "stack": ".NET 10 | Redis | Kubernetes | xUnit",
                "bullets": [
                    "Rebuilt a single-machine WPF application as a multi-pod service. Independently designed and implemented the main service and its tests.",
                    "Implemented table leases with Redis and Lua so acquire, renew, and release are atomic, preventing two pods from taking the same table and processing its signals twice.",
                    "Used supervisor-worker scheduling with one DI scope per table. A failed renewal stops its worker; state-pattern and TimeProvider tests cover eight table states and the scheduling core.",
                    "Removed plaintext credentials and connection strings from version control; Kubernetes Secrets now inject them at deployment time.",
                ],
            },
            {
                "heading": "Chat Platform Audit Logging | 2026",
                "stack": "Go | Gin | Redis Streams | ClickHouse | Uber Fx",
                "bullets": [
                    "Delivered the system end to end, from evaluating options and writing the design to production release, so auditors can answer who changed what and when.",
                    "Sent records through a Redis stream and consumer group before ClickHouse, keeping audit work off the request path; used daily partitions and TTL-based retention.",
                    "Collected HTTP meaning in middleware and before/after snapshots in services, then merged both paths. Replaced raw IDs and enums with names auditors can read directly.",
                    "Used closed types with shared validation so invalid query values return 400. Kept the backend timezone-agnostic with a loose backstop while the frontend owns the precise boundary.",
                ],
            },
            {
                "heading": "Physical Track Control & Firmware | 2024 - 2026",
                "stack": "Python | SPI | UART / RF | Raspberry Pi | Flask | OpenTelemetry",
                "bullets": [
                    "Sole developer of the control software and monitoring UI for eight physical marble tracks, covering sensors, gates, race flow, and OBS scene switching.",
                    "Drove MCP23S17 I/O expanders over SPI to read up to 28 optical sensors, auto-detected two board generations, and provided a simulation fallback when hardware is absent.",
                    "Layered retries, reinitialisation, circuit checks, and resource cleanup around lossy RF links so the system can recover from device faults without manual intervention.",
                    "Isolated eight track-specific flows behind strategy and factory patterns. Three systemd services keep track control running even if the monitoring UI fails.",
                ],
            },
            {
                "heading": "Marble Race Result Judging | 2024 - 2026",
                "stack": "Python | YOLO | Roboflow | PyTorch | OpenCV | ONNX | FastAPI",
                "bullets": [
                    "Built the production system independently: model training, judging logic, query API, and on-site interface. It replaced manual video review.",
                    "Trained each ball as a separate class to avoid multi-object tracking ID switches, then modelled drop judging as a four-state machine.",
                    "Expressed thresholds in time rather than frames. Two-stage confirmation, a survival threshold, and stale cleanup separately absorb missed detections, false positives, and ghost tracks.",
                    "Ranked by the last detection time rather than confirmation time to preserve fairness, and ran inference on a separate thread to keep the on-site UI responsive.",
                ],
            },
        ],
        "footer": "Jack Wu | Backend Engineer",
    },
}


class ResumeDocTemplate(BaseDocTemplate):
    def __init__(self, filename: Path, *, data: dict, font_regular: str, **kwargs):
        super().__init__(str(filename), **kwargs)
        self.resume_data = data
        self.resume_font = font_regular
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="resume-frame",
        )
        self.addPageTemplates(PageTemplate(id="resume", frames=[frame], onPage=self._draw_page))

    def _draw_page(self, canvas, doc):
        data = self.resume_data
        canvas.saveState()
        canvas.setTitle(data["title"])
        canvas.setAuthor("Jack Wu / Wu Cheng-Ju")
        canvas.setSubject("Backend Engineer Resume")
        canvas.setCreator("ReportLab resume generator")
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(self.leftMargin, 20 * mm, A4[0] - self.rightMargin, 20 * mm)
        canvas.setFont(self.resume_font, 7.3)
        canvas.setFillColor(SOFT)
        canvas.drawString(self.leftMargin, 14.2 * mm, data["footer"])
        canvas.drawRightString(A4[0] - self.rightMargin, 14.2 * mm, f"{canvas.getPageNumber()} / 2")
        canvas.restoreState()


def register_fonts() -> tuple[str, str, str, str]:
    fonts_dir = Path("C:/Windows/Fonts")
    required = {
        "ResumeZH": fonts_dir / "msjh.ttc",
        "ResumeZHBold": fonts_dir / "msjhbd.ttc",
        "ResumeEN": fonts_dir / "arial.ttf",
        "ResumeENBold": fonts_dir / "arialbd.ttf",
    }
    missing = [str(path) for path in required.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Required resume fonts are missing: " + ", ".join(missing))
    for name, path in required.items():
        pdfmetrics.registerFont(TTFont(name, str(path), subfontIndex=0))
    pdfmetrics.registerFontFamily("ResumeZH", normal="ResumeZH", bold="ResumeZHBold")
    pdfmetrics.registerFontFamily("ResumeEN", normal="ResumeEN", bold="ResumeENBold")
    return "ResumeZH", "ResumeZHBold", "ResumeEN", "ResumeENBold"


def styles_for(language: str, font_regular: str, font_bold: str) -> dict[str, ParagraphStyle]:
    wrap = "CJK" if language == "zh" else None
    return {
        "name": ParagraphStyle("name", fontName=font_bold, fontSize=23, leading=26, textColor=INK, spaceAfter=1.5 * mm, wordWrap=wrap),
        "role": ParagraphStyle("role", fontName=font_bold, fontSize=11.2, leading=13.5, textColor=ACCENT, spaceAfter=2.2 * mm, wordWrap=wrap),
        "contact": ParagraphStyle("contact", fontName=font_regular, fontSize=8.6, leading=11.5, textColor=SOFT, alignment=TA_CENTER, spaceAfter=2.5 * mm, wordWrap=wrap),
        "section": ParagraphStyle("section", fontName=font_bold, fontSize=10.8, leading=13.2, textColor=ACCENT, spaceBefore=2.5 * mm, spaceAfter=0.8 * mm, wordWrap=wrap),
        "summary": ParagraphStyle("summary", fontName=font_regular, fontSize=9.3, leading=13.2, textColor=INK, spaceAfter=1.8 * mm, wordWrap=wrap),
        "heading": ParagraphStyle("heading", fontName=font_bold, fontSize=9.8, leading=12.4, textColor=INK, spaceBefore=1.8 * mm, spaceAfter=0.7 * mm, wordWrap=wrap),
        "stack": ParagraphStyle("stack", fontName=font_regular, fontSize=8.1, leading=10.3, textColor=SOFT, spaceAfter=0.8 * mm, wordWrap=wrap),
        "bullet": ParagraphStyle("bullet", fontName=font_regular, fontSize=8.85, leading=11.8, textColor=INK, leftIndent=4.4 * mm, firstLineIndent=0, bulletIndent=0.8 * mm, bulletFontName=font_regular, bulletFontSize=7.1, spaceAfter=0.7 * mm, wordWrap=wrap),
        "skill": ParagraphStyle("skill", fontName=font_regular, fontSize=8.7, leading=11.2, textColor=INK, spaceAfter=0.4 * mm, wordWrap=wrap),
        "meta": ParagraphStyle("meta", fontName=font_regular, fontSize=8.7, leading=11.2, textColor=INK, wordWrap=wrap),
    }


def section(title: str, styles: dict[str, ParagraphStyle]) -> list[Flowable]:
    return [
        Paragraph(title, styles["section"]),
        HRFlowable(width="100%", thickness=0.55, color=LINE, spaceBefore=0, spaceAfter=1.1 * mm),
    ]


def bullet_list(items: Iterable[str], styles: dict[str, ParagraphStyle]) -> list[Flowable]:
    return [Paragraph(item, styles["bullet"], bulletText="•") for item in items]


def build_story(data: dict, styles: dict[str, ParagraphStyle]) -> list[Flowable]:
    contact = (
        '<link href="mailto:hotrabbit1016@gmail.com"><font color="#234A6D">hotrabbit1016@gmail.com</font></link>'
        '  |  <link href="tel:+886955684107"><font color="#234A6D">+886 955 684 107</font></link>'
        '  |  <link href="https://hotrabbit1016.github.io/resume/"><font color="#234A6D">hotrabbit1016.github.io/resume</font></link>'
    )
    story: list[Flowable] = [
        Paragraph(data["name"], styles["name"]),
        Paragraph(data["role"], styles["role"]),
        Paragraph(contact, styles["contact"]),
        HRFlowable(width="100%", thickness=1.1, color=ACCENT, spaceBefore=0, spaceAfter=1.5 * mm),
    ]
    story.extend(section(data["summary_title"], styles))
    story.append(Paragraph(data["summary"], styles["summary"]))
    story.extend(section(data["experience_title"], styles))
    for job in data["experience"]:
        block: list[Flowable] = [Paragraph(job["heading"], styles["heading"])]
        block.extend(bullet_list(job["bullets"], styles))
        story.append(KeepTogether(block))
    story.extend(section(data["skills_title"], styles))
    for label, value in data["skills"]:
        story.append(Paragraph(f"<b>{label}:</b> {value}", styles["skill"]))
    story.extend(section(data["education_title"], styles))
    story.append(Paragraph(data["education"], styles["meta"]))
    story.append(PageBreak())
    story.extend(section(data["projects_title"], styles))
    story.append(Spacer(1, 0.7 * mm))
    for project in data["projects"]:
        block = [
            Paragraph(project["heading"], styles["heading"]),
            Paragraph(project["stack"], styles["stack"]),
        ]
        block.extend(bullet_list(project["bullets"], styles))
        block.append(Spacer(1, 1.4 * mm))
        story.append(KeepTogether(block))
    return story


def add_pdf_metadata(source: Path, destination: Path, data: dict) -> None:
    reader = PdfReader(str(source))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.root_object[NameObject("/Lang")] = TextStringObject(data["lang"])
    writer.add_metadata(
        {
            "/Title": data["title"],
            "/Author": "Jack Wu / Wu Cheng-Ju",
            "/Subject": "Backend Engineer Resume",
            "/Keywords": "Backend Engineer, C#, .NET, Go, Python, Kubernetes, Redis, Computer Vision",
            "/Creator": "ReportLab resume generator",
        }
    )
    with destination.open("wb") as stream:
        writer.write(stream)


def generate(language: str, fonts: tuple[str, str, str, str]) -> Path:
    zh_regular, zh_bold, en_regular, en_bold = fonts
    font_regular, font_bold = (zh_regular, zh_bold) if language == "zh" else (en_regular, en_bold)
    data = RESUMES[language]
    style_map = styles_for(language, font_regular, font_bold)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    draft = TEMP_DIR / f"resume-{language}-draft.pdf"
    doc = ResumeDocTemplate(
        draft,
        data=data,
        font_regular=font_regular,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=13.5 * mm,
        bottomMargin=24 * mm,
        title=data["title"],
        author="Jack Wu / Wu Cheng-Ju",
        subject="Backend Engineer Resume",
    )
    doc.build(build_story(data, style_map))
    add_pdf_metadata(draft, data["output"], data)
    draft.unlink(missing_ok=True)
    return data["output"]


def main() -> None:
    fonts = register_fonts()
    outputs = [generate("zh", fonts), generate("en", fonts)]
    for output in outputs:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
