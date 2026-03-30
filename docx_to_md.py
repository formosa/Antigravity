import mammoth
import markdownify

docx_path = r".agent\assets\proposals\active\v6.3\ddr_ref_manual_v6.3(Kimi).docx"
md_path = r".agent\assets\proposals\active\v6.3\ddr_ref_manual_v6.3(Kimi).md"

with open(docx_path, "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html_content = result.value
    messages = result.messages
    if messages:
        print("Mammoth warnings:", messages)

# Convert HTML to Markdown
md_content = markdownify.markdownify(html_content, heading_style="ATX", bullets="-", code_language="python")

with open(md_path, "w", encoding="utf-8") as md_file:
    md_file.write(md_content)

print(f"Successfully converted {docx_path} to {md_path}")
print(f"File length: {len(md_content)} chars")
