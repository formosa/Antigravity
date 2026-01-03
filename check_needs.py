import json
import os
path = r'c:\AI\10162025\maggie\Antigravity\docs\_build\json\needs.json'
if os.path.exists(path):
    with open(path) as f:
        data = json.load(f)
    needs = data['versions']['0.1']['needs']
    if 'TDD-4.1' in needs:
        print(f"Found TDD-4.1: {needs['TDD-4.1']['type']}")
    else:
        print("TDD-4.1 NOT found in needs.json")

    if 'ISP-4.1' in needs:
        print(f"Found ISP-4.1: {needs['ISP-4.1']['type']}")
        print(f"Links for ISP-4.1: {needs['ISP-4.1']['links']}")
else:
    print("File not found")
