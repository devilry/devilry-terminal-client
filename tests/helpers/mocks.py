
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

feedbackset_mock_examiner_and_student = """
[
  {
    "id": 10,
    "group_id": 10,
    "created_datetime": "2016-02-06T15:10:23.061430",
    "feedbackset_type": "first_attempt",
    "is_last_in_group": true,
    "deadline_datetime": "2040-02-14T12:30:00",
    "created_by_fullname": null
  }
]
"""

feedbackset_list_mock_examiner_and_student = """
[
  {
    "id": 10,
    "group_id": 10,
    "created_datetime": "2016-02-06T15:10:23.061430",
    "feedbackset_type": "first_attempt",
    "is_last_in_group": true,
    "deadline_datetime": "2040-02-14T12:30:00",
    "created_by_fullname": null
  },
  {
    "id": 11,
    "group_id": 11,
    "created_datetime": "2016-02-06T15:10:32.192129",
    "feedbackset_type": "first_attempt",
    "is_last_in_group": true,
    "deadline_datetime": "2040-03-15T23:59:00",
    "created_by_fullname": null
  }
]
"""
