# API Contracts

The REST API between the React frontend and the FastAPI backend. Each request and
response shape below is defined as a Pydantic schema in `backend/app/schemas/`. The
schema name is listed with every endpoint.

> Status: designed in #9. The endpoints are not implemented yet.

## Conventions

- **JSON keys are camelCase** (`courseCode`, `planCourses`). The Python code uses
  snake_case (`course_code`). The schemas convert between the two with
  `alias_generator=to_camel`.
- **IDs are integers.** The frontend's `Course.id` in `frontend/src/types/course.ts`
  is currently a `string` and should change to `number`.
- **Term codes** are SFU's 4-digit codes: `1` + 2-digit year + starting month.
  `1251` = Spring 2025, `1254` = Summer 2025, `1257` = Fall 2025.
- **Timestamps** are ISO 8601 strings, e.g. `"2026-01-15T18:30:00Z"`.
- **`null`** means a value is missing or doesn't apply, e.g. a course with no
  designation.
- **`credits` is never `null`.** It is `0` when SFU lists no units for a course.
  The backend stores missing units as `0` (see `Course` in
  `backend/app/models/courses.py`).
- **Users:** `/plans` endpoints act on the signed-in user's plans. Authentication is
  not designed yet, so no endpoint takes a user ID.

## Endpoints

| Method | Path | Request body | Success response |
|---|---|---|---|
| GET | `/courses` | none | `200` list of `CourseSummary` |
| GET | `/courses/{course_id}` | none | `200` `CourseResponse` |
| GET | `/terms` | none | `200` list of `TermRead` |
| GET | `/plans` | none | `200` list of `PlanResponse` |
| POST | `/plans` | `PlanCreate` | `201` `PlanDetailResponse` |
| GET | `/plans/{plan_id}` | none | `200` `PlanDetailResponse` |
| PATCH | `/plans/{plan_id}` | `PlanUpdate` | `200` `PlanResponse` |
| DELETE | `/plans/{plan_id}` | none | `204` no body |
| POST | `/plans/{plan_id}/courses` | `PlanCourseCreate` | `201` `PlanCourseRead` |
| PATCH | `/plans/{plan_id}/courses/{plan_course_id}` | `PlanCourseUpdate` | `200` `PlanCourseRead` |
| DELETE | `/plans/{plan_id}/courses/{plan_course_id}` | none | `204` no body |
| GET | `/programs/{program_code}/requirements` | none | `200` list of `ProgramRequirementResponse` |

---

### Courses

#### `GET /courses`

Returns every course. The frontend loads the list once and filters it in the
browser, so there is no search or pagination yet.

Response `200`, a list of `CourseSummary`:

```json
[
  { "id": 1, "courseCode": "CMPT 120", "title": "Introduction to Computing Science and Programming I", "credits": 3 },
  { "id": 12, "courseCode": "CMPT 225", "title": "Data Structures and Programming", "credits": 3 }
]
```

`credits` is `0` when SFU lists no units for the course. The frontend should show
this as "units not listed", not "0 credits".

#### `GET /courses/{course_id}`

Returns one course's full details. Errors: `404` if the course doesn't exist.

Response `200`, a `CourseResponse` (`CourseSummary` plus these fields):

```json
{
  "id": 12,
  "courseCode": "CMPT 225",
  "title": "Data Structures and Programming",
  "credits": 3,
  "description": "Introduction to a variety of practical and important data structures...",
  "degreeLevel": "UGRD",
  "designation": "Quantitative",
  "prerequisitesText": "(MACM 101 and (CMPT 125, CMPT 129 or CMPT 135)) or (ENSC 251 and ENSC 252), all with a minimum grade of C-.",
  "corequisitesText": null,
  "prerequisites": [
    {
      "groupNumber": 1,
      "requiredCourse": { "id": 3, "courseCode": "CMPT 125", "title": "Introduction to Computing Science and Programming II", "credits": 3 }
    }
  ]
}
```

`prerequisitesText` is SFU's original wording and should always be shown to the
user. `prerequisites` is the structured version the app checks. It can't yet
express every rule, such as "(A and B) or (C and D)" or minimum grades.

---

### Terms

#### `GET /terms`

Response `200`, a list of `TermRead`:

```json
[
  { "code": 1257, "year": 2025, "season": "Fall" },
  { "code": 1261, "year": 2026, "season": "Spring" }
]
```

---

### Plans

#### `GET /plans`

Lists the signed-in user's plans, without their courses.

Response `200`, a list of `PlanResponse`:

```json
[
  {
    "id": 7,
    "name": "Graduate in 4 years",
    "version": 3,
    "createdAt": "2026-01-15T18:30:00Z",
    "updatedAt": "2026-02-02T09:12:44Z"
  }
]
```

#### `POST /plans`

Creates a plan.

Request, a `PlanCreate`. `name` is required, 1–255 characters:

```json
{ "name": "Graduate in 4 years" }
```

Response `201`, a `PlanDetailResponse`. A new plan has an empty `planCourses` list.
Errors: `422` if `name` is missing, empty, or too long.

#### `GET /plans/{plan_id}`

Returns one plan with all its courses. Errors: `404` if the plan doesn't exist.

Response `200`, a `PlanDetailResponse` (`PlanResponse` plus `planCourses`):

```json
{
  "id": 7,
  "name": "Graduate in 4 years",
  "version": 3,
  "createdAt": "2026-01-15T18:30:00Z",
  "updatedAt": "2026-02-02T09:12:44Z",
  "planCourses": [
    {
      "id": 41,
      "termCode": 1257,
      "course": { "id": 12, "courseCode": "CMPT 225", "title": "Data Structures and Programming", "credits": 3 }
    }
  ]
}
```

#### `PATCH /plans/{plan_id}`

Renames a plan.

Request, a `PlanUpdate`. `name` is required, 1–255 characters:

```json
{ "name": "Graduate in 5 years" }
```

Response `200`, a `PlanResponse`. Errors: `404` if the plan doesn't exist, `422`
for an invalid name.

#### `DELETE /plans/{plan_id}`

Deletes a plan and all its courses. Response `204` with no body. Errors: `404`.

---

### Courses in a plan

#### `POST /plans/{plan_id}/courses`

Adds a course to a plan in a given term.

Request, a `PlanCourseCreate`:

```json
{ "courseId": 12, "termCode": 1257 }
```

Response `201`, a `PlanCourseRead`:

```json
{
  "id": 41,
  "termCode": 1257,
  "course": { "id": 12, "courseCode": "CMPT 225", "title": "Data Structures and Programming", "credits": 3 }
}
```

Errors: `404` if the plan, course or term doesn't exist; `422` if a field is
missing or the wrong type.

#### `PATCH /plans/{plan_id}/courses/{plan_course_id}`

Moves a course in a plan to a different term.

Request, a `PlanCourseUpdate`:

```json
{ "termCode": 1261 }
```

Response `200`, a `PlanCourseRead`. Errors: `404`, `422`.

#### `DELETE /plans/{plan_id}/courses/{plan_course_id}`

Removes a course from a plan. Response `204` with no body. Errors: `404`.

---

### Program requirements

#### `GET /programs/{program_code}/requirements`

Lists the requirements for a program, e.g. `CMPT-MAJOR`. Errors: `404` if the
program doesn't exist.

Response `200`, a list of `ProgramRequirementResponse`:

```json
[
  {
    "id": 1,
    "programCode": "CMPT-MAJOR",
    "name": "Calculus",
    "minCredits": null,
    "minCourses": 2,
    "courses": [
      { "course": { "id": 20, "courseCode": "MATH 150", "title": "Calculus I with Review", "credits": 4 } },
      { "course": { "id": 21, "courseCode": "MATH 152", "title": "Calculus II", "credits": 3 } }
    ]
  }
]
```

A requirement is met when the student has at least `minCourses` of the listed
courses and/or at least `minCredits` credits from them, whichever are set.

## Errors

Errors return an `ErrorResponse`:

```json
{ "detail": "Plan not found" }
```

| Status | Meaning |
|---|---|
| `404` | The resource doesn't exist |
| `422` | The request body or path failed validation. FastAPI returns `detail` as a list of `{ "loc", "msg", "type" }` objects |
| `401` | Not signed in. Applies once authentication is added |
