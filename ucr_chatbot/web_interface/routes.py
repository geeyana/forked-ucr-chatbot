from flask import (
    Blueprint,
    render_template,
)
from ucr_chatbot.db.models import Session, engine, Courses, ParticipatesIn
from sqlalchemy import select


bp = Blueprint("web_routes", __name__)

user_email = "test@ucr.edu"


@bp.route("/")
def course_selection():
    """Renders the main landing page with a list of the user's courses.

    This route queries the database to find all courses the current user
    is enrolled in and passes that list to the landing_page.html
    template for display.

    :return: The rendered HTML content of the landing page.
    """
    print("web_interface")
    with Session(engine) as session:
        stmt = (
            select(Courses)
            .join(ParticipatesIn, Courses.id == ParticipatesIn.course_id)
            .where(ParticipatesIn.email == user_email)
        )
        courses = session.execute(stmt).scalars().all()

    return render_template(
        "landing_page.html",
        courses=courses,
    )


@bp.route("/new_conversation/<int:course_id>/chat")
def new_conversation(course_id: int):
    """Redirects to a page with a new conversation for a course.
    :param course_id: The id of the course for which a conversation will be initialized.
    """

    return render_template("conversation.html")


@bp.route("/conversation/<int:conversation_id>")
def conversation(conversation_id: int):
    """Responds with page where a student can interact with a chatbot for a course.

    :param conversation_id: The id of the conversation to be send back to the user.
    """
    print("web con")
    return render_template(
        "conversation.html",
        title="Landing Page",
        body=f"Chat with me about the course2 for which the conversation with id {conversation_id} exists.",
    )


@bp.route("/course/<int:course_id>/documents")
def course_documents(course_id: int):
    """Responds with a page where a course administrator can add more documents
    to the course for use by the retrieval-augmented generation system.
    :param course_id: The id of the course for which a conversation will be initialized.
    """
    return render_template(
        "base.html",
        title="Landing Page",
        body=f"These are the documents for the course with id {course_id}",
    )
