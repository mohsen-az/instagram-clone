# Instagram Clone (Django Rest API)

# Endpoints
### User:
    - api/auth/profile/                                   - Retrieve|Update
    - api/auth/profile/follower/                          - List
    - api/auth/profile/following/                         - List
    - api/auth/profile/invitation/                        - List
    - api/auth/profile/<str:username>/                    - Retrieve
### Relation:
    - api/relation/friendships/<int:pk>/follow/           - Create
    - api/relation/friendships/<int:pk>/unfollow/         - Delete
    - api/relation/friendships/<int:pk>/accept/           - Create
    - api/relation/friendships/<int:pk>/reject/           - Delete
### Content:
    - api/content/post/add/                               - Create
    - api/content/<str:username>/posts/                   - List
    - api/content/<str:username>/posts/<int:pk>/          - Retrieve
    - api/content/<str:username>/posts/<int:pk>/comments/ - List
    - api/content/<str:username>/posts/<int:pk>/likes/    - List
### Activity:
    - api/activity/comments/<int:pk>/add/                 - Create
    - api/activity/likes/<int:pk>/like/                   - Create
    - api/activity/likes/<int:pk>/unlike/                 - Delete

# Run this project
`[sudo] docker compose up --build`
