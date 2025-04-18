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


def _safe_string(text, default=""):
    """Safely convert to string and strip whitespace."""
    return text.strip() if isinstance(text, str) else default


def _create_bullet_point(pdf, text, indent=5):
    """Create a bullet point with text."""
    if not _safe_string(text):
        pdf.ln()
        return

    pdf.cell(indent, 5, "-", 0, 0)
    available_width = pdf.w - pdf.l_margin - pdf.r_margin - indent
    if available_width > pdf.get_string_width("W"):
        pdf.multi_cell(available_width, 5, f" {text}")
        pdf.set_x(pdf.l_margin)
    else:
        pdf.ln()


def _add_section_header(pdf, title, is_modern=False):
    """Add a section header to the PDF."""
    if not _safe_string(title):
        return

    if is_modern:
        pdf.set_font(pdf.font_family, "B", 14)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, title.upper(), 0, 1, "L", True)
        pdf.ln(2)
    else:
        pdf.set_font(pdf.font_family, "B", 12)
        pdf.cell(0, 10, title.upper(), 0, 1, "")
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)


def _format_description_list(description):
    """Format and validate a description list."""
    if isinstance(description, list):
        return [
            d.strip() for d in description if d and isinstance(d, str) and d.strip()
        ]
    return []


def _add_title_with_date(pdf, title, date, font_size=11, is_right_aligned=True):
    """Add a title with an optional date aligned to the right."""
    title_text = _safe_string(title)
    date_text = _safe_string(date)

    if not title_text:
        return

    pdf.set_font(pdf.font_family, "B", font_size)

    if date_text and is_right_aligned:
        date_width = pdf.get_string_width(date_text) + 10
        title_width = pdf.w - pdf.l_margin - pdf.r_margin - date_width
        pdf.cell(title_width, 6, title_text, 0, 0)
        pdf.set_font(pdf.font_family, "", font_size - 1)
        pdf.cell(date_width, 6, date_text, 0, 1, "R")
    else:
        pdf.cell(0, 6, title_text, 0, 1)


def _process_bullet_points(pdf, description):
    """Process bullet points from a description."""
    if not description:
        return

    pdf.set_font(pdf.font_family, "", 10)

    if isinstance(description, list):
        descriptions = _format_description_list(description)
        for bullet in descriptions:
            _create_bullet_point(pdf, bullet)
    elif isinstance(description, str) and description.strip():
        pdf.multi_cell(0, 5, description.strip())


def _add_contact_info(pdf, contact_items, separator=" - ", is_modern=False):
    """Add contact information to the PDF."""
    if not isinstance(contact_items, list):
        return

    pdf.set_font(pdf.font_family, "", 10)

    contact = [
        item.strip()
        for item in contact_items
        if item and isinstance(item, str) and item.strip()
    ]

    if contact:
        contact_text = separator.join(contact)
        pdf.cell(0, 5, contact_text, 0, 1, "C")
        pdf.ln(5 if not is_modern else 10)


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
        return create_resume(segments, font_family, segment_order)
    elif template == "modern":
        return create_modern_resume(segments, font_family, segment_order)
    else:
        return create_resume(segments, font_family)


def _add_summary_section(pdf, summary, is_modern=False):
    """Add summary section to the PDF."""
    if not _safe_string(summary):
        return

    _add_section_header(pdf, "Professional Summary", is_modern)
    pdf.set_font(
        pdf.font_family, "" if not is_modern else "I", 10 if not is_modern else 11
    )
    pdf.multi_cell(0, 5, summary.strip())
    pdf.ln(5)


def _add_experience_section(pdf, experience_items, is_modern=False):
    """Add experience section to the PDF."""
    if not experience_items:
        return

    _add_section_header(pdf, "Professional Experience", is_modern)
    pdf.set_font(pdf.font_family, "", 10)

    for item in experience_items:
        if isinstance(item, dict):
            company = _safe_string(item.get("company"))
            title_text = _safe_string(item.get("title"))
            date = _safe_string(item.get("date"))
            workplace = _safe_string(item.get("location"))

            if is_modern:
                pdf.set_font(pdf.font_family, "B", 12)
                if company:
                    pdf.cell(0, 6, company, 0, 1)

                pdf.set_font(pdf.font_family, "", 11)
                if title_text:
                    title_width = pdf.w - pdf.l_margin - pdf.r_margin
                    if date:
                        date_width = pdf.get_string_width(date) + 10
                        title_width -= date_width
                        pdf.cell(title_width, 5, title_text, 0, 0)
                        pdf.cell(date_width, 5, date, 0, 1, "R")
                    else:
                        pdf.cell(title_width, 5, title_text, 0, 1)

                if workplace:
                    pdf.set_font(pdf.font_family, "I", 10)
                    pdf.cell(0, 5, workplace, 0, 1)
            else:
                pdf.set_font(pdf.font_family, "B", 11)
                first_line = title_text
                if company:
                    if first_line:
                        first_line = first_line + " at " + company
                    else:
                        first_line = company

                if first_line:
                    pdf.cell(0, 6, first_line.strip(), 0, 1)

                if workplace:
                    pdf.set_font(pdf.font_family, "", 10)
                    pdf.cell(pdf.get_string_width(workplace) + 5, 5, workplace, 0, 0)

                if date:
                    pdf.set_x(pdf.w - pdf.get_string_width(date) - 10)
                    pdf.cell(pdf.get_string_width(date), 5, date, 0, 1, "R")
                elif workplace:
                    pdf.ln()

            _process_bullet_points(pdf, item.get("description"))
            pdf.ln(5 if is_modern else 2)

    pdf.ln(3)


def _add_education_section(pdf, education_items, is_modern=False):
    """Add education section to the PDF."""
    if not education_items:
        return

    _add_section_header(pdf, "Education", is_modern)
    pdf.set_font(pdf.font_family, "", 10)

    for item in education_items:
        if isinstance(item, dict):
            institute = _safe_string(item.get("institute"))
            degree = _safe_string(item.get("title"))
            location = _safe_string(item.get("location"))
            date = _safe_string(item.get("date"))

            if is_modern:
                if institute:
                    pdf.set_font(pdf.font_family, "B", 12)
                    pdf.cell(0, 6, institute, 0, 1)

                if degree:
                    pdf.set_font(pdf.font_family, "", 11)
                    date_width = pdf.get_string_width(date) + 10 if date else 0
                    degree_width = pdf.w - pdf.l_margin - pdf.r_margin - date_width
                    pdf.cell(degree_width, 5, degree, 0, 0)

                    if date:
                        pdf.cell(date_width, 5, date, 0, 1, "R")
                    else:
                        pdf.ln()

                if location:
                    pdf.set_font(pdf.font_family, "I", 10)
                    pdf.cell(0, 5, location, 0, 1)
            else:
                if degree:
                    pdf.set_font(pdf.font_family, "B", 11)
                    date_width = pdf.get_string_width(date) + 10 if date else 0
                    degree_width = pdf.w - pdf.l_margin - pdf.r_margin - date_width
                    pdf.cell(degree_width, 6, degree, 0, 0)

                    if date:
                        pdf.set_font(pdf.font_family, "", 10)
                        pdf.set_x(pdf.w - pdf.r_margin - pdf.get_string_width(date))
                        pdf.cell(pdf.get_string_width(date), 6, date, 0, 1, "R")
                    else:
                        pdf.ln()

                pdf.set_font(pdf.font_family, "", 10)
                if institute:
                    institute_width = pdf.w - pdf.l_margin - pdf.r_margin
                    if location:
                        institute_width -= pdf.get_string_width(location) + 10
                    pdf.cell(institute_width, 5, institute, 0, 0)

                if location:
                    pdf.cell(
                        pdf.get_string_width(location) + 10, 5, location, 0, 1, "R"
                    )
                elif institute:
                    pdf.ln()

            _process_bullet_points(pdf, item.get("description"))
            pdf.ln(3 if is_modern else 2)

    pdf.ln(3)


def _add_skills_section(pdf, skills_items, is_modern=False):
    """Add skills section to the PDF."""
    if not skills_items:
        return

    _add_section_header(pdf, "Skills", is_modern)
    pdf.set_font(pdf.font_family, "", 10)

    if isinstance(skills_items, list):
        skills = [
            item.strip()
            for item in skills_items
            if isinstance(item, str) and item.strip()
        ]

        if skills:
            skills_text = " | " if is_modern else " - "
            skills_text = skills_text.join(skills)

            available_width = pdf.w - pdf.l_margin - pdf.r_margin
            pdf.multi_cell(available_width, 5, skills_text)

    pdf.ln(3)


def _add_certifications_section(pdf, cert_items, is_modern=False):
    """Add certifications section to the PDF."""
    if not cert_items:
        return

    _add_section_header(pdf, "Certifications", is_modern)
    pdf.set_font(pdf.font_family, "", 10)

    if isinstance(cert_items, list):
        for item in cert_items:
            if isinstance(item, dict):
                title_text = _safe_string(item.get("title"))
                issuer = _safe_string(item.get("issuer"))
                date = _safe_string(item.get("date"))

                if is_modern:
                    if title_text:
                        pdf.set_font(pdf.font_family, "B", 11)
                        pdf.cell(0, 6, title_text, 0, 1)

                    if issuer:
                        pdf.set_font(pdf.font_family, "", 10)
                        issuer_width = pdf.w - pdf.l_margin - pdf.r_margin
                        if date:
                            date_width = pdf.get_string_width(date) + 10
                            issuer_width -= date_width
                            pdf.cell(issuer_width, 5, f"Issued by: {issuer}", 0, 0)
                            pdf.cell(date_width, 5, date, 0, 1, "R")
                        else:
                            pdf.cell(issuer_width, 5, f"Issued by: {issuer}", 0, 1)

                    # if credentialId:
                    #     pdf.set_font(pdf.font_family, "I", 9)
                    #     pdf.cell(0, 5, f"Credential ID: {credentialId}", 0, 1)
                else:
                    pdf.set_font(pdf.font_family, "B", 11)
                    date_width = pdf.get_string_width(date) + 10 if date else 0
                    title_width = pdf.w - pdf.l_margin - pdf.r_margin - date_width

                    if title_text:
                        if issuer:
                            title_text = f"{title_text} by {issuer}"
                        pdf.cell(title_width, 5, title_text, 0, 0)

                    if date:
                        pdf.set_font(pdf.font_family, "", 10)
                        pdf.cell(date_width, 5, date, 0, 1, "R")
                    else:
                        pdf.ln()

                    # if credentialId:
                    #     pdf.set_x(pdf.l_margin)
                    #     pdf.multi_cell(0, 5, credentialId)

                _process_bullet_points(pdf, item.get("description"))
                pdf.ln(3)
            elif isinstance(item, str) and item.strip():
                pdf.cell(
                    5 if is_modern else 0,
                    5,
                    "-" if is_modern else f"- {item.strip()}",
                    0,
                    0 if is_modern else 1,
                )
                if is_modern:
                    pdf.cell(0, 5, item.strip(), 0, 1)

    pdf.ln(3)


def _add_open_source_section(pdf, open_source_items, is_modern=False):
    """Add open source section to the PDF."""
    if not open_source_items:
        return

    _add_section_header(pdf, "Open Source", is_modern)
    pdf.set_font(pdf.font_family, "", 10)

    if isinstance(open_source_items, list):
        for item in open_source_items:
            if isinstance(item, dict):
                title_text = _safe_string(item.get("title"))
                url = _safe_string(item.get("url"))

                if title_text:
                    pdf.set_font(pdf.font_family, "B", 11)
                    if url:
                        text_color = pdf.text_color
                        pdf.set_text_color(
                            0, 102 if is_modern else 0, 204 if is_modern else 255
                        )
                        pdf.cell(0, 6, title_text, 0, 1, link=url)
                        pdf.set_text_color(text_color[0], text_color[1], text_color[2])
                    else:
                        pdf.cell(0, 6, title_text, 0, 1)

                _process_bullet_points(pdf, item.get("description"))
                pdf.ln(3 if is_modern else 2)
            elif isinstance(item, str) and item.strip():
                pdf.cell(
                    5 if is_modern else 0,
                    5,
                    "-" if is_modern else f"- {item.strip()}",
                    0,
                    0 if is_modern else 1,
                )
                if is_modern:
                    pdf.cell(0, 5, item.strip(), 0, 1)

    pdf.ln(3)


def create_resume(segments, font_family="Times", segment_order=None):
    """Create a resume PDF using the classic template."""
    if not isinstance(segments, dict):
        segments = {}

    font_family = font_family if isinstance(font_family, str) else "Times"

    if segment_order is None:
        segment_order = [
            "experience",
            "skills",
            "certifications",
            "open_source",
            "education",
        ]

    pdf = PDF(font_family=font_family)
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font(font_family, "B", 16)
    name = _safe_string(segments.get("name"))
    pdf.cell(0, 10, name, 0, 1, "C")

    _add_contact_info(pdf, segments.get("contact"), separator=" - ", is_modern=False)

    if "summary" in segments:
        _add_summary_section(pdf, segments["summary"], is_modern=False)
    for segment in segment_order:
        if segment == "summary" and "summary" in segments:
            _add_summary_section(pdf, segments["summary"], is_modern=False)
        elif segment == "experience" and "experience" in segments:
            _add_experience_section(pdf, segments["experience"], is_modern=False)
        elif segment == "education" and "education" in segments:
            _add_education_section(pdf, segments["education"], is_modern=False)
        elif segment == "skills" and "skills" in segments:
            _add_skills_section(pdf, segments["skills"], is_modern=False)
        elif segment == "certifications" and "certifications" in segments:
            _add_certifications_section(
                pdf, segments["certifications"], is_modern=False
            )
        elif segment == "open_source" and "open_source" in segments:
            _add_open_source_section(pdf, segments["open_source"], is_modern=False)

    output_file = generate_file_path()
    pdf.output(output_file)
    return output_file


def create_modern_resume(segments, font_family="Times", segment_order=None):
    """Create a resume PDF using the modern template."""
    if not isinstance(segments, dict):
        segments = {}

    if segment_order is None:
        segment_order = [
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
    name = _safe_string(segments.get("name"))
    pdf.cell(0, 10, name, 0, 1, "C")

    line_width = pdf.get_string_width(name) * 0.8
    line_start = (pdf.w - line_width) / 2
    pdf.line(line_start, pdf.get_y(), line_start + line_width, pdf.get_y())
    pdf.ln(5)

    _add_contact_info(pdf, segments.get("contact"), separator=" | ", is_modern=True)

    if "summary" in segments:
        _add_summary_section(pdf, segments["summary"], is_modern=True)
    for section in segment_order:
        if section == "experience" and "experience" in segments:
            _add_experience_section(pdf, segments["experience"], is_modern=True)
        elif section == "education" and "education" in segments:
            _add_education_section(pdf, segments["education"], is_modern=True)
        elif section == "skills" and "skills" in segments:
            _add_skills_section(pdf, segments["skills"], is_modern=True)
        elif section == "certifications" and "certifications" in segments:
            _add_certifications_section(pdf, segments["certifications"], is_modern=True)
        elif section == "open_source" and "open_source" in segments:
            _add_open_source_section(pdf, segments["open_source"], is_modern=True)

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
