import os
import tempfile

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.models.assessment import Assessment
from app.utils.pdf_parser import extract_text_from_pdf


# ---------------------------------------------------------
# Analyze Resume
# ---------------------------------------------------------

def analyze_resume(
    db: Session,
    file: UploadFile
):
    # ----------------------------------------
    # Validate File
    # ----------------------------------------

    if not file.filename.lower().endswith(".pdf"):
        raise ValueError(
            "Only PDF files are allowed."
        )

    # ----------------------------------------
    # Save Temporary File
    # ----------------------------------------

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(file.file.read())

        temp_path = temp_file.name

    # ----------------------------------------
    # Extract Text
    # ----------------------------------------

    extracted_text = extract_text_from_pdf(
        temp_path
    )

    os.remove(temp_path)

    # ----------------------------------------
    # Normalize Resume
    # ----------------------------------------

    resume_text = extracted_text.lower()

    # ----------------------------------------
    # Fetch Skills
    # ----------------------------------------

    skills = (
        db.query(Skill)
        .all()
    )

    matched_skills = []
    missing_skills = []

    # ----------------------------------------
    # Match Skills
    # ----------------------------------------

    for skill in skills:

        if skill.name.lower() in resume_text:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    # ----------------------------------------
    # Readiness Score
    # ----------------------------------------

    total_skills = len(skills)

    if total_skills == 0:

        readiness_score = 0

    else:

        readiness_score = round(

            (
                len(matched_skills)
                /
                total_skills
            ) * 100,

            2
        )

    # ----------------------------------------
    # Recommended Assessments
    # ----------------------------------------

    recommended_assessments = []

    for skill in matched_skills:

        assessments = (

            db.query(Assessment)

            .filter(

                Assessment.skill_id == skill.id,

                Assessment.user_id == skill.user_id,

                Assessment.is_active == True

            )

            .all()

        )

        for assessment in assessments:

            recommended_assessments.append({

                "id": assessment.id,

                "title": assessment.title,

                "description": assessment.description,

                "duration_minutes": assessment.duration_minutes,

                "passing_score": assessment.passing_score

            })

    # ----------------------------------------
    # Return Response
    # ----------------------------------------

    return {

        "matched_skills": [

            skill.name

            for skill in matched_skills

        ],

        "missing_skills": [

            skill.name

            for skill in missing_skills

        ],

        "matched_count": len(

            matched_skills

        ),

        "missing_count": len(

            missing_skills

        ),

        "readiness_score": readiness_score,

        "extracted_text": extracted_text,

        "recommended_assessments": recommended_assessments

    }