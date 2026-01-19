# How to Check Logged-In Users

## 🎯 Quick Overview

Your application now tracks all user logins, activity, and sessions automatically!

---

## 📊 **Method 1: Check Backend Terminal (Easiest)**

Just look at your backend terminal window where you ran `start-backend.bat`

### What You'll See:

```
✅ USER LOGIN: John Doe (john@example.com) at 2026-01-20 14:30:45
==================================================
BACKEND: Data Generation Complete
User: john@example.com
Number of samples: 300
...
👋 USER LOGOUT: John Doe (john@example.com)
```

**Every login shows:**
- ✅ USER LOGIN: [Name] ([Email]) at [Time]

**Every data generation shows:**
- User: [Email]

**Every logout shows:**
- 👋 USER LOGOUT: [Name] ([Email])

---

## 🌐 **Method 2: Use API Endpoints**

### **See Currently Active Users:**

**Browser/Postman:**
```
GET http://localhost:8000/api/auth/admin/active-users
```

**Response:**
```json
{
  "active_users": [
    {
      "email": "john@example.com",
      "full_name": "John Doe",
      "login_time": "2026-01-20T14:30:45",
      "last_activity": "2026-01-20T14:35:20",
      "minutes_since_activity": 2.5,
      "status": "active"
    }
  ],
  "total_active": 1,
  "timestamp": "2026-01-20T14:37:50"
}
```

---

### **See Login/Logout History:**

**Browser/Postman:**
```
GET http://localhost:8000/api/auth/admin/activity-log
```

**Response:**
```json
{
  "activities": [
    {
      "email": "john@example.com",
      "full_name": "John Doe",
      "action": "login",
      "timestamp": "2026-01-20T14:30:45",
      "time_ago": "7 minutes ago"
    },
    {
      "email": "jane@example.com",
      "full_name": "Jane Smith",
      "action": "logout",
      "timestamp": "2026-01-20T14:25:30",
      "time_ago": "12 minutes ago"
    }
  ],
  "total_events": 45,
  "showing": 50
}
```

---

### **See All Registered Users:**

**Browser/Postman:**
```
GET http://localhost:8000/api/auth/admin/all-users
```

**Response:**
```json
{
  "users": [
    {
      "email": "john@example.com",
      "full_name": "John Doe",
      "created_at": "2026-01-15T10:20:30",
      "is_active": true,
      "last_activity": "2026-01-20T14:35:20"
    },
    {
      "email": "jane@example.com",
      "full_name": "Jane Smith",
      "created_at": "2026-01-18T09:15:00",
      "is_active": false,
      "last_activity": null
    }
  ],
  "total_users": 2,
  "active_now": 1
}
```

---

## 🔧 **Method 3: Using Browser Console**

Open your browser console (F12) and run:

```javascript
// Get your token
const token = localStorage.getItem('token')

// Check active users
fetch('http://localhost:8000/api/auth/admin/active-users', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(data => {
  console.log('Active Users:', data.active_users.length)
  console.table(data.active_users)
})

// Check activity log
fetch('http://localhost:8000/api/auth/admin/activity-log', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(data => {
  console.log('Recent Activity:')
  console.table(data.activities)
})
```

---

## 📱 **Method 4: Using Postman**

1. **Open Postman**
2. **Create New Request:**
   - Method: GET
   - URL: `http://localhost:8000/api/auth/admin/active-users`
3. **Add Authorization:**
   - Type: Bearer Token
   - Token: [Your JWT token from login]
4. **Send Request**

---

## 🎨 **Quick Reference Table**

| Endpoint | What It Shows | Updates |
|----------|--------------|---------|
| Terminal | Real-time login/logout/activity | Live |
| `/admin/active-users` | Who is online now | Every API call |
| `/admin/activity-log` | Login/logout history | Every login/logout |
| `/admin/all-users` | All registered users | On registration |

---

## ⏰ **Activity Tracking Rules**

- **Active**: Last activity within 5 minutes
- **Idle**: Last activity within 30 minutes
- **Offline**: No activity for 30+ minutes
- **Updates**: Every time user makes any API request

---

## 💡 **Tips**

1. **Keep backend terminal visible** - easiest way to monitor
2. **Active session expires** after 30 minutes of inactivity
3. **JWT token expires** after 24 hours
4. **Activity log** stores all login/logout events forever (until server restart)

---

## 🔒 **Security Note**

⚠️ Currently using **in-memory storage** - all data resets when backend restarts!

For production, you should:
- Add a database (PostgreSQL, MongoDB, etc.)
- Store sessions in Redis
- Add admin authentication for these endpoints
- Add rate limiting

---

## 🎯 **Example: Check Who's Using Your Tool Right Now**

```bash
# Quick check in PowerShell/CMD:
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/auth/admin/active-users
```

Or just **look at your backend terminal** - you'll see every login! ✨
