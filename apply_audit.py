import sys

file_path = r'c:\AI\10162025\maggie\Antigravity\.agent\assets\proposals\future\DDR_v4_Logic_Audit.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('**Description:**', '**Description:** <span style=\"color:violet\">***Verified and Validated***</span>')

target_str = 'The ORL migration (5 rules to GPCL-R6–R10)'
replacement_str = 'The ORL migration (<span style=\"color:red\">~~5 rules~~</span> <span style=\"color:#00BFFF\">*7 rules*</span> to GPCL-R6–R10)'
content = content.replace(target_str, replacement_str)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
