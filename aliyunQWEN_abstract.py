import os
from dashscope import Generation
import fitz  # PyMuPDF for PDF text extraction

def extract_text_from_pdf(file_path):
    try:
        with fitz.open(file_path) as doc:
            return "\n".join(page.get_text("text") for page in doc)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def summarize_with_qwen(text, api_key, model='qwen-plus'):
    if not text:
        print("No text to summarize.")
        return None

    response = Generation.call(
        api_key=api_key,
        model=model,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f'请为以下文档生成中文摘要：\n{text}'}#prompt
        ]
    )

    if response.status_code == 200:
        return response.output.text
    else:
        print(f"API Error: {response.status_code}, {response.message}")
        return None

def save_summary_to_txt(summary, output_file_path):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"Summary saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving summary to {output_file_path}: {e}")

def process_and_summarize_pdfs(pdf_files, api_key, model='qwen-plus', output_dir="summaries"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdf_file in pdf_files:
        if not os.path.isfile(pdf_file):
            print(f"File {pdf_file} does not exist or is not a file.")
            continue

        print(f"Processing {pdf_file}...")
        text = extract_text_from_pdf(pdf_file)
        if text:
            summary = summarize_with_qwen(text, api_key, model)
            if summary:
                # 构建输出文件名，例如：input.pdf -> summaries/input_summary.txt
                base_name = os.path.splitext(os.path.basename(pdf_file))[0]
                output_file_path = os.path.join(output_dir, f"{base_name}_summary.txt")
                save_summary_to_txt(summary, output_file_path)
            else:
                print("Failed to generate summary.")
        else:
            print(f"Failed to extract text from {pdf_file}.")

if __name__ == "__main__":
    # 设置环境变量或直接在这里定义
    api_key = os.environ.get('QWEN_MAX_API_KEY')  # 确保设置了正确的环境变量名称

    if not api_key:
        raise ValueError("API key is missing. Please set the QWEN_MAX_API_KEY environment variable.")

    # 指定要处理的PDF文件路径列表
    pdf_files = [
        "",  # 替换为你的第一个PDF文件路径
        "", # 替换为你的第二个PDF文件路径
        # 添加更多PDF文件路径...
    ]
    # 定义输出摘要的路径
    output_directory = r""  # 替换为你想要保存摘要的目录路径

    # 调用函数处理并生成多个PDF文件的摘要
    process_and_summarize_pdfs(pdf_files, api_key, model='qwen-plus', output_dir=output_directory)