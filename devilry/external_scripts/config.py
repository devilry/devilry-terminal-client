from .assignment.cli import Assignment
from .assignment_group.cli import AssignmentGroup
from .feedbackset.cli import Feedbackset
from .group_comment.cli import GroupComment

#: Installed scripts goes here.
INSTALLED_SCRIPTS = [
    Assignment,
    AssignmentGroup,
    Feedbackset,
    GroupComment
]
