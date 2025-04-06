"""PDF generation service."""

from fpdf import FPDF

from utils.utils import generate_file_path


class PDF(FPDF):
    def __init__(self, title="", font_family="Arial"):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.title = title if isinstance(title, str) else ""
        self.font_family = font_family if isinstance(font_family, str) else "Arial"
        self.set_margins(10, 10 if not self.title else 30, 10)

        self.set_font(self.font_family, "")

    def header(self):
        if self.title and isinstance(self.title, str):
            self.set_font(self.font_family, "B", 12)
            self.cell(0, 10, self.title, 0, 0, "C")
            self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_family, "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")


def create_resume_with_template(
    segments, template="classic", font_family="Times", segment_order=None
):
    """Create a resume PDF with a specified template.

    Args:
        segments (dict): Resume data segments
        template (str): Template name ('classic' or 'modern')
        font_family (str): Font family to use
        segment_order (list): Order of segments to display (defaults to experience, skills,
                              certifications, open_source, education)

    Returns:
        str: Path to the generated PDF file
    """
    if template == "classic":
        return create_resume(segments, font_family)
    elif template == "modern":
        return create_modern_resume(segments, font_family, segment_order)
    else:
        return create_resume(segments, font_family)


def create_resume(segments, font_family="Times"):
    """Create a resume PDF using the classic template."""
    if not isinstance(segments, dict):
        segments = {}

    font_family = font_family if isinstance(font_family, str) else "Times"

    pdf = PDF(font_family=font_family)
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font(font_family, "B", 16)
    name = segments.get("name", "")
    name = name.strip() if isinstance(name, str) else ""
    pdf.cell(0, 10, name, 0, 1, "C")

    if "contact" in segments and isinstance(segments["contact"], list):
        pdf.set_font(font_family, "", 10)

        contact = [
            item.strip()
            for item in segments["contact"]
            if item and isinstance(item, str) and item.strip()
        ]
        if contact:
            contact_text = " - ".join(contact)
            pdf.cell(0, 5, contact_text, 0, 1, "C")
            pdf.ln(5)

    def add_section_header(title):
        if not title or not isinstance(title, str):
            return
        pdf.set_font(font_family, "B", 12)
        pdf.cell(0, 10, title.upper(), 0, 1, "")
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

    def add_summary_section(summary):
        if not summary or not isinstance(summary, str):
            return

        add_section_header("PROFESSIONAL SUMMARY")
        pdf.set_font(font_family, "", 10)
        pdf.multi_cell(0, 5, summary.strip())
        pdf.ln(5)

    def add_experience_section(experience_items):
        if not experience_items:
            return

        add_section_header("PROFESSIONAL EXPERIENCE")
        pdf.set_font(font_family, "", 10)

        for item in experience_items:
            if isinstance(item, dict):
                company = item.get("company", "")
                title_text = item.get("title", "")
                pdf.set_font(font_family, "B", 11)
                first_line = ""
                if isinstance(title_text, str) and title_text.strip():
                    first_line = title_text.strip()
                if company and isinstance(company, str) and company.strip():
                    if first_line:
                        first_line = first_line + " at " + company.strip()
                    else:
                        first_line = company.strip()

                pdf.cell(0, 6, first_line.strip(), 0, 1)

                workplace = item.get("location", "")

                date = item.get("date", "")
                date = date.strip() if isinstance(date, str) else ""

                if workplace:
                    pdf.set_font(font_family, "", 10)
                    if workplace and isinstance(workplace, str) and workplace.strip():
                        pdf.cell(
                            pdf.get_string_width(workplace.strip()) + 5,
                            5,
                            workplace.strip(),
                            0,
                            0,
                        )
                if date:
                    pdf.set_x(pdf.w - pdf.get_string_width(date) - 10)
                    pdf.cell(pdf.get_string_width(date), 5, date, 0, 1, "R")
                elif workplace:
                    pdf.ln()

                description = item.get("description", "")
                if description:
                    pdf.set_font(font_family, "", 10)
                    if isinstance(description, list):
                        descriptions = [
                            d.strip()
                            for d in description
                            if d and isinstance(d, str) and d.strip()
                        ]
                        for bullet in descriptions:
                            pdf.cell(5, 5, "-", 0, 0)
                            if bullet and len(bullet) > 0:
                                available_width = (
                                    pdf.w - pdf.l_margin - pdf.r_margin - 5
                                )
                                if available_width > pdf.get_string_width("W"):
                                    pdf.multi_cell(available_width, 5, f" {bullet}")
                                    pdf.set_x(pdf.l_margin)
                                else:
                                    pdf.ln()
                            else:
                                pdf.ln()
                pdf.ln(2)

        pdf.ln(5)

    def add_education_section(education_items):
        if not education_items:
            return

        add_section_header("EDUCATION")
        pdf.set_font(font_family, "", 10)

        for item in education_items:
            if isinstance(item, dict):
                degree = item.get("title", "")
                institute = item.get("institute", "")
                location = item.get("location", "")
                date = item.get("date", "")
                date = date.strip() if isinstance(date, str) else ""

                pdf.set_font(font_family, "B", 11)
                if isinstance(degree, str) and degree.strip():
                    date_width = pdf.get_string_width(date) + 10 if date else 0
                    degree_width = pdf.w - pdf.l_margin - pdf.r_margin - date_width
                    pdf.cell(degree_width, 6, degree.strip(), 0, 0)

                if date:
                    pdf.set_font(font_family, "", 10)
                    pdf.set_x(pdf.w - pdf.r_margin - pdf.get_string_width(date))
                    pdf.cell(pdf.get_string_width(date), 6, date, 0, 1, "R")
                else:
                    pdf.ln()

                pdf.set_font(font_family, "", 10)
                if institute and isinstance(institute, str) and institute.strip():
                    institute_width = pdf.w - pdf.l_margin - pdf.r_margin
                    if location and isinstance(location, str) and location.strip():
                        institute_width -= pdf.get_string_width(location.strip()) + 10
                    pdf.cell(institute_width, 5, institute.strip(), 0, 0)

                if location and isinstance(location, str) and location.strip():
                    pdf.cell(
                        pdf.get_string_width(location.strip()) + 10,
                        5,
                        location.strip(),
                        0,
                        1,
                        "R",
                    )
                elif institute:
                    pdf.ln()

                description = item.get("description", "")
                if description:
                    pdf.set_font(font_family, "", 10)
                    if isinstance(description, list):
                        descriptions = [
                            d.strip()
                            for d in description
                            if d and isinstance(d, str) and d.strip()
                        ]
                        for bullet in descriptions:
                            pdf.cell(5, 5, "-", 0, 0)
                            if bullet and len(bullet) > 0:
                                available_width = (
                                    pdf.w - pdf.l_margin - pdf.r_margin - 5
                                )
                                pdf.multi_cell(available_width, 5, f" {bullet}")
                                pdf.set_x(pdf.l_margin)
                            else:
                                pdf.ln()
                pdf.ln(2)
        pdf.ln(5)

    def add_skills_section(skills_items):
        if not skills_items:
            return

        add_section_header("SKILLS")
        pdf.set_font(font_family, "", 10)

        if isinstance(skills_items, list):
            string_skills = []

            for item in skills_items:
                string_skills.append(item)

            if string_skills:
                skills_text = " - ".join(string_skills)
                pdf.multi_cell(0, 5, skills_text)
                pdf.ln(2)

        pdf.ln(5)

    def add_certifications_section(cert_items):
        if not cert_items:
            return

        add_section_header("CERTIFICATIONS")
        if isinstance(cert_items, list):
            for item in cert_items:
                if isinstance(item, dict):
                    title_text = item.get("title", "")
                    issuer = item.get("issuer", "")
                    date = item.get("date", "")

                    pdf.set_font(font_family, "B", 11)

                    date_width = pdf.get_string_width(date) + 10 if date else 0
                    title_width = pdf.w - pdf.l_margin - pdf.r_margin - date_width

                    if isinstance(title_text, str) and title_text.strip():
                        if issuer and isinstance(issuer, str) and issuer.strip():
                            title_text = f"{title_text.strip()} by {issuer.strip()}"
                        pdf.cell(title_width, 5, title_text.strip(), 0, 0)

                    if date:
                        pdf.set_font(font_family, "", 10)
                        pdf.cell(date_width, 5, date, 0, 1, "R")
                    else:
                        pdf.ln()

                    description = item.get("description", "")
                    if description:
                        if isinstance(description, list):
                            for bullet in description:
                                if isinstance(bullet, str) and bullet.strip():
                                    pdf.cell(5, 5, "-", 0, 0)
                                    pdf.multi_cell(0, 5, f" {bullet.strip()}")
                        elif isinstance(description, str) and description.strip():
                            pdf.multi_cell(0, 5, description.strip())
                    credentialId = item.get("credentialId", "")
                    if credentialId:
                        pdf.set_x(pdf.l_margin)
                        pdf.multi_cell(0, 5, credentialId.strip())
                    pdf.ln(3)

                elif isinstance(item, str) and item.strip():
                    pdf.cell(0, 5, f"- {item.strip()}", 0, 1)

        pdf.ln(5)

    def add_open_source_section(open_source_items):
        if not open_source_items:
            return

        add_section_header("OPEN SOURCE")
        pdf.set_font(font_family, "", 10)

        if isinstance(open_source_items, list):
            for item in open_source_items:
                if isinstance(item, dict):
                    title_text = item.get("title", "")
                    url = item.get("url", "")

                    if isinstance(title_text, str) and title_text.strip():
                        pdf.set_font(font_family, "B", 11)
                        if url and isinstance(url, str) and url.strip():
                            text_color = pdf.text_color

                            pdf.set_text_color(0, 0, 255)
                            pdf.cell(0, 6, title_text.strip(), 0, 1, link=url.strip())

                            pdf.set_text_color(
                                text_color[0], text_color[1], text_color[2]
                            )
                        else:
                            pdf.cell(0, 6, title_text.strip(), 0, 1)

                    description = item.get("description", "")
                    if description:
                        pdf.set_font(font_family, "", 10)
                        if isinstance(description, list):
                            for bullet in description:
                                if isinstance(bullet, str) and bullet.strip():
                                    pdf.cell(5, 5, "-", 0, 0)
                                    pdf.multi_cell(0, 5, f" {bullet.strip()}")
                        elif isinstance(description, str) and description.strip():
                            pdf.multi_cell(0, 5, description.strip())

                    pdf.ln(2)
                elif isinstance(item, str) and item.strip():
                    pdf.cell(0, 5, f"- {item.strip()}", 0, 1)

        pdf.ln(5)

    if "summary" in segments and isinstance(segments["summary"], str):
        add_summary_section(segments["summary"])

    if "experience" in segments:
        add_experience_section(segments["experience"])

    if "skills" in segments:
        add_skills_section(segments["skills"])

    if "certifications" in segments:
        add_certifications_section(segments["certifications"])

    if "open_source" in segments:
        add_open_source_section(segments["open_source"])

    if "education" in segments:
        add_education_section(segments["education"])

    output_file = generate_file_path()
    pdf.output(output_file)
    return output_file


def create_modern_resume(segments, font_family="Times", segment_order=None):
    """Create a resume PDF using the modern template."""
    if not isinstance(segments, dict):
        segments = {}

    if segment_order is None:
        segment_order = [
            "summary",
            "experience",
            "skills",
            "certifications",
            "open_source",
            "education",
        ]

    font_family = font_family if isinstance(font_family, str) else "Times"

    pdf = PDF(font_family=font_family)
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font(font_family, "B", 18)
    name = segments.get("name", "")
    name = name.strip() if isinstance(name, str) else ""
    pdf.cell(0, 10, name, 0, 1, "C")

    line_width = pdf.get_string_width(name) * 0.8
    line_start = (pdf.w - line_width) / 2
    pdf.line(line_start, pdf.get_y(), line_start + line_width, pdf.get_y())
    pdf.ln(5)

    if "contact" in segments and isinstance(segments["contact"], list):
        pdf.set_font(font_family, "", 10)
        contact = [
            item.strip()
            for item in segments["contact"]
            if item and isinstance(item, str) and item.strip()
        ]
        if contact:
            contact_text = " | ".join(contact)
            pdf.cell(0, 5, contact_text, 0, 1, "C")
            pdf.ln(10)

    def add_section_header(title):
        if not title or not isinstance(title, str):
            return
        pdf.set_font(font_family, "B", 14)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, title.upper(), 0, 1, "L", True)
        pdf.ln(2)

    def add_summary_section(summary):
        if not summary or not isinstance(summary, str):
            return

        add_section_header("Professional Summary")
        pdf.set_font(font_family, "I", 11)
        pdf.multi_cell(0, 5, summary.strip())
        pdf.ln(5)

    def add_experience_section(experience_items):
        if not experience_items:
            return

        add_section_header("Professional Experience")
        pdf.set_font(font_family, "", 10)

        for item in experience_items:
            if isinstance(item, dict):
                company = item.get("company", "")
                title_text = item.get("title", "")
                pdf.set_font(font_family, "B", 12)

                if company and isinstance(company, str) and company.strip():
                    pdf.cell(0, 6, company.strip(), 0, 1)

                pdf.set_font(font_family, "", 11)
                date = item.get("date", "")
                date = date.strip() if isinstance(date, str) else ""

                if isinstance(title_text, str) and title_text.strip():
                    title_width = pdf.w - pdf.l_margin - pdf.r_margin
                    if date:
                        date_width = pdf.get_string_width(date) + 10
                        title_width -= date_width
                        pdf.cell(title_width, 5, title_text.strip(), 0, 0)
                        pdf.cell(date_width, 5, date, 0, 1, "R")
                    else:
                        pdf.cell(title_width, 5, title_text.strip(), 0, 1)

                workplace = item.get("location", "")
                if workplace and isinstance(workplace, str) and workplace.strip():
                    pdf.set_font(font_family, "I", 10)
                    pdf.cell(0, 5, workplace.strip(), 0, 1)

                description = item.get("description", "")
                if description:
                    pdf.set_font(font_family, "", 10)
                    if isinstance(description, list):
                        descriptions = [
                            d.strip()
                            for d in description
                            if d and isinstance(d, str) and d.strip()
                        ]
                        for bullet in descriptions:
                            pdf.cell(5, 5, "-", 0, 0)
                            if bullet and len(bullet) > 0:
                                available_width = (
                                    pdf.w - pdf.l_margin - pdf.r_margin - 5
                                )
                                pdf.multi_cell(available_width, 5, f" {bullet}")
                                pdf.set_x(pdf.l_margin)
                pdf.ln(5)

        pdf.ln(3)

    def add_education_section(education_items):
        if not education_items:
            return

        add_section_header("Education")
        pdf.set_font(font_family, "", 10)

        for item in education_items:
            if isinstance(item, dict):
                institute = item.get("institute", "")
                degree = item.get("title", "")
                location = item.get("location", "")
                date = item.get("date", "")

                if institute and isinstance(institute, str) and institute.strip():
                    pdf.set_font(font_family, "B", 12)
                    pdf.cell(0, 6, institute.strip(), 0, 1)

                if isinstance(degree, str) and degree.strip():
                    pdf.set_font(font_family, "", 11)
                    date_width = pdf.get_string_width(date) + 10 if date else 0
                    degree_width = pdf.w - pdf.l_margin - pdf.r_margin - date_width
                    pdf.cell(degree_width, 5, degree.strip(), 0, 0)

                    if date and isinstance(date, str) and date.strip():
                        pdf.cell(date_width, 5, date.strip(), 0, 1, "R")
                    else:
                        pdf.ln()

                if location and isinstance(location, str) and location.strip():
                    pdf.set_font(font_family, "I", 10)
                    pdf.cell(0, 5, location.strip(), 0, 1)

                description = item.get("description", "")
                if description:
                    pdf.set_font(font_family, "", 10)
                    if isinstance(description, list):
                        descriptions = [
                            d.strip()
                            for d in description
                            if d and isinstance(d, str) and d.strip()
                        ]
                        for bullet in descriptions:
                            pdf.cell(5, 5, "-", 0, 0)
                            if bullet and len(bullet) > 0:
                                available_width = (
                                    pdf.w - pdf.l_margin - pdf.r_margin - 5
                                )
                                pdf.multi_cell(available_width, 5, f" {bullet}")
                                pdf.set_x(pdf.l_margin)
                pdf.ln(3)

        pdf.ln(3)

    def add_skills_section(skills_items):
        if not skills_items:
            return

        add_section_header("Skills")
        pdf.set_font(font_family, "", 10)

        if isinstance(skills_items, list):
            skills = [
                item.strip()
                for item in skills_items
                if isinstance(item, str) and item.strip()
            ]

            if skills:
                skills_text = " | ".join(skills)

                available_width = pdf.w - pdf.l_margin - pdf.r_margin
                pdf.multi_cell(available_width, 5, skills_text)

        pdf.ln(3)

    def add_certifications_section(cert_items):
        if not cert_items:
            return

        add_section_header("Certifications")
        pdf.set_font(font_family, "", 10)

        if isinstance(cert_items, list):
            for item in cert_items:
                if isinstance(item, dict):
                    title_text = item.get("title", "")
                    issuer = item.get("issuer", "")
                    date = item.get("date", "")

                    if isinstance(title_text, str) and title_text.strip():
                        pdf.set_font(font_family, "B", 11)
                        pdf.cell(0, 6, title_text.strip(), 0, 1)

                    if issuer and isinstance(issuer, str) and issuer.strip():
                        pdf.set_font(font_family, "", 10)
                        issuer_width = pdf.w - pdf.l_margin - pdf.r_margin
                        if date and isinstance(date, str) and date.strip():
                            date_width = pdf.get_string_width(date) + 10
                            issuer_width -= date_width
                            pdf.cell(
                                issuer_width, 5, f"Issued by: {issuer.strip()}", 0, 0
                            )
                            pdf.cell(date_width, 5, date, 0, 1, "R")
                        else:
                            pdf.cell(
                                issuer_width, 5, f"Issued by: {issuer.strip()}", 0, 1
                            )

                    credentialId = item.get("credentialId", "")
                    if (
                        credentialId
                        and isinstance(credentialId, str)
                        and credentialId.strip()
                    ):
                        pdf.set_font(font_family, "I", 9)
                        pdf.cell(0, 5, f"Credential ID: {credentialId.strip()}", 0, 1)

                    description = item.get("description", "")
                    if description:
                        pdf.set_font(font_family, "", 10)
                        if isinstance(description, list):
                            for bullet in description:
                                if isinstance(bullet, str) and bullet.strip():
                                    pdf.cell(5, 5, "-", 0, 0)
                                    pdf.multi_cell(0, 5, f" {bullet.strip()}")
                        elif isinstance(description, str) and description.strip():
                            pdf.multi_cell(0, 5, description.strip())
                    pdf.ln(3)

                elif isinstance(item, str) and item.strip():
                    pdf.cell(5, 5, "-", 0, 0)
                    pdf.cell(0, 5, item.strip(), 0, 1)

        pdf.ln(3)

    def add_open_source_section(open_source_items):
        if not open_source_items:
            return

        add_section_header("Open Source")
        pdf.set_font(font_family, "", 10)

        if isinstance(open_source_items, list):
            for item in open_source_items:
                if isinstance(item, dict):
                    title_text = item.get("title", "")
                    url = item.get("url", "")

                    if isinstance(title_text, str) and title_text.strip():
                        pdf.set_font(font_family, "B", 11)
                        if url and isinstance(url, str) and url.strip():
                            text_color = pdf.text_color
                            pdf.set_text_color(0, 102, 204)
                            pdf.cell(0, 6, title_text.strip(), 0, 1, link=url.strip())
                            pdf.set_text_color(
                                text_color[0], text_color[1], text_color[2]
                            )
                        else:
                            pdf.cell(0, 6, title_text.strip(), 0, 1)

                    description = item.get("description", "")
                    if description:
                        pdf.set_font(font_family, "", 10)
                        if isinstance(description, list):
                            for bullet in description:
                                if isinstance(bullet, str) and bullet.strip():
                                    pdf.cell(5, 5, "-", 0, 0)
                                    pdf.multi_cell(0, 5, f" {bullet.strip()}")
                        elif isinstance(description, str) and description.strip():
                            pdf.multi_cell(0, 5, description.strip())
                    pdf.ln(3)

                elif isinstance(item, str) and item.strip():
                    pdf.cell(5, 5, "-", 0, 0)
                    pdf.cell(0, 5, item.strip(), 0, 1)

        pdf.ln(3)

    for section in segment_order:
        if section == "summary" and "summary" in segments:
            add_summary_section(segments["summary"])
        elif section == "experience" and "experience" in segments:
            add_experience_section(segments["experience"])
        elif section == "education" and "education" in segments:
            add_education_section(segments["education"])
        elif section == "skills" and "skills" in segments:
            add_skills_section(segments["skills"])
        elif section == "certifications" and "certifications" in segments:
            add_certifications_section(segments["certifications"])
        elif section == "open_source" and "open_source" in segments:
            add_open_source_section(segments["open_source"])

    output_file = generate_file_path()
    pdf.output(output_file)
    return output_file


def create_cover_letter(text, title, font_family="Times"):
    """Create a cover letter PDF."""
    if not isinstance(text, str):
        text = ""

    title = title if isinstance(title, str) else ""
    font_family = font_family if isinstance(font_family, str) else "Arial"

    pdf = PDF(title, font_family=font_family)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font(font_family, "", 12)

    closing_keywords = ["sincerely", "regards"]

    paragraphs = text.split("\n\n")

    for paragraph in paragraphs:
        lines = paragraph.split("\n")

        is_signature = False
        if len(lines) >= 2:
            for keyword in closing_keywords:
                if keyword in lines[0].lower():
                    is_signature = True
                    break

        if is_signature:
            pdf.cell(0, 5, lines[0], 0, 1)
            pdf.ln(1)
            pdf.set_x(pdf.l_margin)
            for i in range(1, len(lines)):
                pdf.cell(0, 5, lines[i], 0, 1)
        else:
            for line in lines:
                if isinstance(line, str):
                    available_width = pdf.w - pdf.l_margin - pdf.r_margin
                    pdf.multi_cell(available_width, 5, line)
        pdf.ln(5)

    output_file = generate_file_path()
    pdf.output(output_file)
    return output_file
