from .assignment.cli import Assignment
from .assignment_group.cli import AssignmentGroup

#: Installed plugins goes here.
INSTALLED_SCRIPTS = [
    Assignment,
    AssignmentGroup,
]
