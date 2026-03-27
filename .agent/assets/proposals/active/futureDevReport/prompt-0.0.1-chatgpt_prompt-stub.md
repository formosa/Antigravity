# CREATE IMAGE:  Technical Visualization

Create a new image of a technical visualization designed to enhance understanding of the following CONTEXT.


## CONTEXT:

~~~md
%content%


~~~



## ROLE: 

You are a senior systems architect and technical visualization specialist. Produce a single, publication-ready technical diagram derived ONLY from the attached DDR documentation excerpt.


## SOURCE OF TRUTH:

Use exclusively the attached context excerpt. Do not invent tiers, rules, fields, edge types, operations, or relationships not explicitly present. If information is missing, omit it visually rather than guessing.


## OBJECTIVE:

Generate a high-precision, data-analytics–styled visualization that maximizes structural understanding, traceability clarity, and abstraction boundaries.



## VISUAL STYLE (STRICT):

• White or ultra-light background, subtle grid or graph-paper texture  

• Thin vector lines, sharp geometry, consistent stroke weights  

• Muted professional palette (blues, slate, charcoal, soft accent color)  

• Modern sans-serif typography, clear hierarchy (Title / Tier / Node / Edge labels)  

• No decorative illustrations; only structured technical forms  

• Use alignment grids and even spacing for architectural symmetry  



## STRUCTURAL RULES:

1. Represent tiers as clearly separated horizontal layers ordered by abstraction level.  

2. Represent nodes as labeled containers including: ID, Tier, Title (if present).  

3. Represent edge types with distinct visual encoding:

   - derives → solid line with arrow

   - constrains → dashed line

   - implements → double-line arrow

   - extends → dotted overlay line

4. Enforce DAG directionality visually (top-to-bottom or left-to-right).  

5. If a merge node exists (e.g., SAL), visually emphasize convergence.  

6. Display rule IDs (e.g., AX-#, SIL-R#, CIT-R#) in compact annotation badges.  



## ACCURACY CONTROLS:

• Cross-check every visual element against explicit text references.  

• Preserve exact terminology and capitalization.  

• No summarization that alters meaning.  

• No inferred relationships beyond what is stated.  



## OUTPUT:

Single high-resolution, technically precise architectural diagram optimized for embedding in formal engineering documentation.