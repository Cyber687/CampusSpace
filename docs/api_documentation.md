# API quick reference

Open `/docs` after starting the app for interactive OpenAPI documentation. Protected endpoints require `Authorization: Bearer <access_token>`.

## Register
`POST /api/v1/auth/register`
```json
{"full_name":"Example Student","email":"student@example.edu","password":"a-strong-password","department":"Engineering"}
```

## Login
`POST /api/v1/auth/login`
```json
{"email":"rohan@student.campusspace.edu","password":"CampusDemo123!"}
```

## Create fault report
`POST /api/v1/fault-reports`
```json
{"category":"Socket / Switch / Light","description":"Socket cover is damaged near the front row.","classroom_id":1,"canteen_id":null,"is_urgent":false}
```

## Verify room
`POST /api/v1/classrooms/1/verifications`
```json
{"reported_status":"Reported Available"}
```

## Check in to canteen
`POST /api/v1/canteens/check-in`
```json
{"qr_identifier":"QR_B25C_FLOOR6"}
```

## Maintenance status update
`PATCH /api/v1/fault-reports/1`
```json
{"status":"In Progress","note":"Inspection started."}
```

## CSV timetable import
Multipart upload with headers `classroom_id,subject_name,day_of_week,start_time,end_time,is_break_slot`.
