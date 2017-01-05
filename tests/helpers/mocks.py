
assignment_mock_student_and_examiner = """
[
  {
    "anonymizationmode": "off",
    "id": 1,
    "long_name": "Assignment 1",
    "period_id": 1,
    "period_short_name": "springaaaa",
    "publishing_time": "2015-12-27T03:35:27.525662",
    "short_name": "assignment1",
    "subject_short_name": "duck1010"
  }
]
"""
assignment_list_mock_student_and_examiner = """
[
  {
    "anonymizationmode": "off",
    "id": 5,
    "long_name": "Assignment 0",
    "period_id": 1,
    "period_short_name": "springaaaa",
    "publishing_time": "2016-02-08T20:58:20.423164",
    "short_name": "assignment0",
    "subject_short_name": "duck1010"
  },
  {
    "anonymizationmode": "off",
    "id": 1,
    "long_name": "Assignment 1",
    "period_id": 1,
    "period_short_name": "springaaaa",
    "publishing_time": "2015-12-27T03:35:27.525662",
    "short_name": "assignment1",
    "subject_short_name": "duck1010"
  }
]
"""

assignment_group_mock_student_and_examiner = """
[
  {
    "id": 9,
    "name": "",
    "assignment_id": 1,
    "assignment_short_name": "assignment1",
    "subject_short_name": "duck1010",
    "period_short_name": "springaaaa",
    "short_displayname": "april@example.com",
    "long_displayname": "April Duck",
    "is_waiting_for_feedback": false,
    "is_waiting_for_deliveries": false,
    "is_corrected": true,
    "candidates": [
      {
        "fullname": "April Duck",
        "shortname": "april@example.com"
      }
    ],
    "examiners": [
      {
        "fullname": "God of thunder and Battle",
        "shortname": "thor@example.com"
      },
      {
        "fullname": "Trickster and god of Mischief",
        "shortname": "loki@example.com"
      }
    ]
  }
]
"""

assignment_group_list_mock_student_and_examiner = """
[
  {
    "id": 9,
    "name": "",
    "assignment_id": 1,
    "assignment_short_name": "assignment1",
    "subject_short_name": "duck1010",
    "period_short_name": "springaaaa",
    "short_displayname": "april@example.com",
    "long_displayname": "April Duck",
    "is_waiting_for_feedback": false,
    "is_waiting_for_deliveries": false,
    "is_corrected": true,
    "candidates": [
      {
        "fullname": "April Duck",
        "shortname": "april@example.com"
      }
    ],
    "examiners": [
      {
        "fullname": "God of thunder and Battle",
        "shortname": "thor@example.com"
      },
      {
        "fullname": "Trickster and god of Mischief",
        "shortname": "loki@example.com"
      }
    ]
  },
  {
    "id": 10,
    "name": "",
    "assignment_id": 2,
    "assignment_short_name": "assignment2",
    "subject_short_name": "duck1010",
    "period_short_name": "springaaaa",
    "short_displayname": "april@example.com",
    "long_displayname": "April Duck",
    "is_waiting_for_feedback": false,
    "is_waiting_for_deliveries": true,
    "is_corrected": false,
    "candidates": [
      {
        "fullname": "April Duck",
        "shortname": "april@example.com"
      }
    ],
    "examiners": []
  }
]
"""
