## Description: <br>
Creates, reads, edits, combines, and validates PowerPoint .pptx presentations with guidance for design, templates, palettes, and QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mebusw](https://clawhub.ai/user/mebusw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to create new PPTX decks, adapt existing templates, extract presentation content, and run content and visual QA before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read presentation content and create or modify files in the workspace. <br>
Mitigation: Confirm target files and output paths before execution, and keep backups of important source presentations. <br>
Risk: Optional image generation or remote image sources may expose presentation intent or introduce unsuitable visuals. <br>
Mitigation: Use local approved assets or ask the agent to disable external image generation when a local-only workflow is required. <br>
Risk: PPTX, Node, Python, and conversion tooling may require dependency installs or shell commands. <br>
Mitigation: Review commands before execution and run the workflow in an isolated workspace with only the required dependencies. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/mebusw/jackyshen-gen-pptx) <br>
- [ClawHub skill page](https://clawhub.ai/mebusw/skills/jackyshen-gen-pptx) <br>
- [PptxGenJS presentation creation guide](creating.md) <br>
- [Presentation editing workflow](editing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets; generated work may include .pptx files, extracted text, images, or intermediate XML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate on workspace presentation files and use optional image generation, package installation, and QA conversion tools.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
