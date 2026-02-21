# Django Blog - Authentication System Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication Features](#authentication-features)
3. [System Architecture](#system-architecture)
4. [User Interaction Flow](#user-interaction-flow)
5. [Detailed Feature Documentation](#detailed-feature-documentation)
6. [Testing Guide](#testing-guide)
7. [Technical Implementation](#technical-implementation)

---

## Overview

This Django blog application implements a comprehensive authentication system using Django's built-in authentication framework (`django.contrib.auth`). The system provides user registration, login, logout, password reset functionality, and user profile management with custom templates.

### Key Components
- **User Registration**: Custom registration form with email validation
- **User Login**: Django's built-in LoginView with custom template
- **User Logout**: Django's built-in LogoutView with custom template
- **Password Reset**: Complete password reset flow with email support
- **User Profile**: View and edit user profile information
- **Profile Pictures**: Upload and manage profile pictures

---

## Authentication Features

### 1. User Registration
- **URL**: `/blog/register/`
- **View**: Custom `register` function view
- **Form**: `RegisterForm` (extends Django's `UserCreationForm`)
- **Features**:
  - Username validation
  - Email address (required)
  - Password strength validation
  - Password confirmation matching
  - Automatic profile creation upon registration

### 2. User Login
- **URL**: `/blog/login/`
- **View**: Django's `LoginView` (class-based view)
- **Template**: `blog/login.html`
- **Features**:
  - Username/password authentication
  - CSRF protection
  - Error message display for invalid credentials
  - Automatic redirect after successful login

### 3. User Logout
- **URL**: `/blog/logout/`
- **View**: Django's `LogoutView` (class-based view)
- **Template**: `blog/logout.html`
- **Features**:
  - Session termination
  - Custom logout confirmation page
  - Supports both GET and POST requests

### 4. Password Reset
- **URLs**:
  - `/blog/password_reset/` - Request password reset
  - `/blog/password_reset/done/` - Confirmation email sent
  - `/blog/password_reset/confirm/<uidb64>/<token>/` - Reset password form
  - `/blog/password_reset/complete/` - Password reset complete
- **Views**: Django's built-in password reset views
- **Features**:
  - Email-based password reset
  - Secure token-based reset links
  - Password validation

### 5. User Profile
- **URL**: `/blog/profile/`
- **View**: `profile` function view (login required)
- **Template**: `blog/profile.html`
- **Features**:
  - Display user information (username, email, full name)
  - Display profile picture
  - Protected route (requires authentication)

### 6. Edit Profile
- **URL**: `/blog/edit_profile/`
- **View**: `edit_profile` function view (login required)
- **Template**: `blog/edit_profile.html`
- **Form**: `UserProfileForm`
- **Features**:
  - Update username, email, first name, last name
  - Upload/update profile picture
  - Image resizing (max 300x300 pixels)
  - Form validation

---

## System Architecture

### Models

#### User Model (Django Built-in)
- Django's default `User` model from `django.contrib.auth.models`
- Fields: username, email, password, first_name, last_name, etc.

#### Profile Model
- **Location**: `blog/models.py`
- **Relationship**: OneToOne with User model
- **Fields**:
  - `user`: OneToOneField to User
  - `profile_picture`: ImageField (optional)
- **Features**:
  - Automatically created when a User is created (via signal)
  - Profile pictures are automatically resized to 300x300 pixels

### Forms

#### RegisterForm
- **Location**: `blog/forms.py`
- **Extends**: `UserCreationForm`
- **Fields**: username, email, password1, password2
- **Validation**: 
  - Email is required
  - Password strength validation
  - Password confirmation matching

#### UserProfileForm
- **Location**: `blog/forms.py`
- **Extends**: `ModelForm`
- **Fields**: username, email, first_name, last_name, profile_picture
- **Features**:
  - Handles both User and Profile model updates
  - Profile picture upload and management

### Views

#### Custom Views
- `register()`: Handles user registration
- `profile()`: Displays user profile (login required)
- `edit_profile()`: Handles profile editing (login required)

#### Django Built-in Views
- `LoginView`: User authentication
- `LogoutView`: User logout
- `PasswordResetView`: Password reset request
- `PasswordResetDoneView`: Reset email sent confirmation
- `PasswordResetConfirmView`: Password reset form
- `PasswordResetCompleteView`: Reset completion confirmation

### URL Configuration
- **Main URLs**: `django_blog/urls.py`
- **App URLs**: `blog/urls.py`
- All authentication URLs are prefixed with `/blog/`

---

## User Interaction Flow

### Registration Flow
1. User navigates to `/blog/register/`
2. User fills out registration form:
   - Username
   - Email address
   - Password
   - Password confirmation
3. Form validation occurs:
   - Username uniqueness check
   - Email format validation
   - Password strength requirements
   - Password match verification
4. If valid:
   - User account is created
   - Profile is automatically created (via signal)
   - User is redirected to login page
5. If invalid:
   - Error messages are displayed
   - User can correct and resubmit

### Login Flow
1. User navigates to `/blog/login/`
2. User enters credentials:
   - Username
   - Password
3. Django authenticates the user
4. If successful:
   - User session is created
   - User is redirected (default: `/accounts/profile/` or next parameter)
5. If unsuccessful:
   - Error message is displayed
   - User can retry

### Logout Flow
1. User clicks logout link (from any authenticated page)
2. User is logged out:
   - Session is terminated
   - User is redirected to logout confirmation page
3. Logout confirmation page displays:
   - "You have been logged out" message
   - Link to login again

### Password Reset Flow
1. User navigates to `/blog/password_reset/`
2. User enters their email address
3. If email exists:
   - Password reset email is sent
   - User sees confirmation page
4. User clicks link in email:
   - Navigates to password reset form
   - Enters new password (twice for confirmation)
5. If valid:
   - Password is updated
   - User sees success message
   - User can login with new password

### Profile Management Flow
1. **View Profile**:
   - User navigates to `/blog/profile/` (must be logged in)
   - Profile information is displayed
   - Profile picture is shown (if uploaded)

2. **Edit Profile**:
   - User navigates to `/blog/edit_profile/` (must be logged in)
   - Form is pre-filled with current information
   - User updates desired fields
   - User can upload new profile picture
   - Form is submitted
   - If valid:
     - User and Profile models are updated
     - Profile picture is resized if needed
     - User is redirected to profile page

---

## Detailed Feature Documentation

### 1. User Registration

#### How It Works
- Uses Django's `UserCreationForm` as base
- Extends form to include email field (required)
- Custom validation ensures email uniqueness and format
- Upon successful registration:
  - User account is created in database
  - Password is hashed using Django's password hashing
  - Profile is automatically created via `post_save` signal
  - User is redirected to login page

#### Form Fields
- **Username**: Required, must be unique
- **Email**: Required, must be valid email format
- **Password**: Required, must meet Django's password requirements
- **Password Confirmation**: Must match password

#### Security Features
- CSRF protection enabled
- Password hashing (not stored in plain text)
- Email validation
- Username uniqueness enforcement

### 2. User Login

#### How It Works
- Uses Django's `LoginView` class-based view
- Authenticates user credentials against database
- Creates user session upon successful authentication
- Handles authentication errors gracefully

#### Authentication Process
1. User submits login form
2. Django validates CSRF token
3. Django authenticates credentials:
   - Checks username exists
   - Verifies password hash matches
4. If successful:
   - Creates session
   - Sets authentication cookie
   - Redirects to next page or default
5. If unsuccessful:
   - Displays error message
   - User can retry

#### Security Features
- CSRF protection
- Session-based authentication
- Secure password verification (hashed comparison)
- Automatic session timeout

### 3. User Logout

#### How It Works
- Uses Django's `LogoutView` class-based view
- Terminates user session
- Clears authentication cookies
- Displays custom logout confirmation page

#### Logout Process
1. User clicks logout link (GET or POST request)
2. Django terminates session:
   - Deletes session data
   - Clears session cookie
3. User is redirected to logout template
4. Logout confirmation is displayed

#### Configuration
- Supports both GET and POST requests (configured in `blog/urls.py`)
- Custom template: `blog/logout.html`
- No redirect URL needed (shows confirmation page)

### 4. Password Reset

#### How It Works
- Multi-step process using Django's password reset views
- Email-based reset system
- Token-based security

#### Reset Process Steps

**Step 1: Request Reset** (`/blog/password_reset/`)
- User enters email address
- System checks if email exists in database
- If exists, generates secure reset token
- Sends email with reset link

**Step 2: Email Sent** (`/blog/password_reset/done/`)
- Confirmation page displayed
- User is instructed to check email

**Step 3: Reset Form** (`/blog/password_reset/confirm/<uidb64>/<token>/`)
- User clicks link from email
- Token is validated
- If valid, password reset form is displayed
- User enters new password (twice)

**Step 4: Reset Complete** (`/blog/password_reset/complete/`)
- Password is updated in database
- Success message displayed
- User can login with new password

#### Security Features
- Time-limited reset tokens
- One-time use tokens
- Base64 encoded user ID
- Secure token generation

### 5. User Profile

#### How It Works
- Protected view (requires authentication)
- Displays user information from User model
- Shows profile picture from Profile model
- Uses `@login_required` decorator

#### Displayed Information
- Username
- Email address
- Full name (first name + last name)
- Profile picture (if uploaded)

#### Access Control
- Only accessible to authenticated users
- Unauthenticated users are redirected to login
- Users can only view their own profile

### 6. Edit Profile

#### How It Works
- Protected view (requires authentication)
- Uses `UserProfileForm` to handle updates
- Updates both User and Profile models
- Handles file uploads for profile pictures

#### Editable Fields
- Username
- Email
- First Name
- Last Name
- Profile Picture

#### Profile Picture Handling
- Image upload to `profile_pictures/` directory
- Automatic resizing to 300x300 pixels (max)
- Uses PIL/Pillow for image processing
- Optional field (can be left empty)

#### Form Processing
1. GET request: Form is displayed with current data
2. POST request:
   - Form validation occurs
   - If valid:
     - User model fields are updated
     - Profile picture is saved to Profile model
     - Image is resized if needed
     - User is redirected to profile page
   - If invalid:
     - Error messages displayed
     - User can correct and resubmit

---

## Testing Guide

### Prerequisites
- Django development server running
- MySQL database configured and migrated
- All dependencies installed

### Test User Registration

#### Test Case 1: Successful Registration
1. Navigate to `http://localhost:8000/blog/register/`
2. Fill in the form:
   - Username: `testuser`
   - Email: `testuser@example.com`
   - Password: `TestPassword123!`
   - Password Confirmation: `TestPassword123!`
3. Click "Register" button
4. **Expected Result**: 
   - Redirected to login page
   - User account created in database
   - Profile automatically created

#### Test Case 2: Registration with Invalid Email
1. Navigate to registration page
2. Fill in form with invalid email (e.g., `notanemail`)
3. Click "Register"
4. **Expected Result**: 
   - Form displays email validation error
   - User account not created

#### Test Case 3: Registration with Mismatched Passwords
1. Navigate to registration page
2. Fill in form with different passwords
3. Click "Register"
4. **Expected Result**: 
   - Form displays password mismatch error
   - User account not created

#### Test Case 4: Registration with Existing Username
1. Navigate to registration page
2. Fill in form with username that already exists
3. Click "Register"
4. **Expected Result**: 
   - Form displays username already exists error
   - User account not created

### Test User Login

#### Test Case 1: Successful Login
1. Navigate to `http://localhost:8000/blog/login/`
2. Enter valid credentials:
   - Username: `testuser`
   - Password: `TestPassword123!`
3. Click "Login" button
4. **Expected Result**: 
   - User is authenticated
   - Redirected to next page or default
   - Session is created

#### Test Case 2: Login with Invalid Credentials
1. Navigate to login page
2. Enter incorrect username or password
3. Click "Login"
4. **Expected Result**: 
   - Error message displayed: "Invalid username or password"
   - User remains on login page
   - No session created

#### Test Case 3: Login with Non-existent User
1. Navigate to login page
2. Enter username that doesn't exist
3. Click "Login"
4. **Expected Result**: 
   - Error message displayed
   - Login fails

### Test User Logout

#### Test Case 1: Successful Logout
1. Login to the application
2. Navigate to any authenticated page
3. Click "Logout" link
4. **Expected Result**: 
   - User is logged out
   - Session is terminated
   - Redirected to logout confirmation page
   - "You have been logged out" message displayed

#### Test Case 2: Access Protected Page After Logout
1. Logout from the application
2. Try to access `/blog/profile/`
3. **Expected Result**: 
   - Redirected to login page
   - Cannot access protected content

### Test Password Reset

#### Test Case 1: Request Password Reset
1. Navigate to `http://localhost:8000/blog/password_reset/`
2. Enter registered email address
3. Click "Submit"
4. **Expected Result**: 
   - Redirected to confirmation page
   - Email sent (if email backend configured)
   - Message: "We've emailed you instructions..."

#### Test Case 2: Password Reset with Invalid Email
1. Navigate to password reset page
2. Enter email that doesn't exist in database
3. Click "Submit"
4. **Expected Result**: 
   - Still shows confirmation (security: doesn't reveal if email exists)
   - No email sent

#### Test Case 3: Complete Password Reset
1. Click password reset link from email
2. Enter new password (twice)
3. Click "Reset Password"
4. **Expected Result**: 
   - Password is updated
   - Success message displayed
   - Can login with new password

### Test User Profile

#### Test Case 1: View Profile (Authenticated)
1. Login to the application
2. Navigate to `http://localhost:8000/blog/profile/`
3. **Expected Result**: 
   - Profile page displays
   - Shows username, email, full name
   - Shows profile picture (if uploaded)

#### Test Case 2: View Profile (Unauthenticated)
1. Logout from the application
2. Try to access `/blog/profile/`
3. **Expected Result**: 
   - Redirected to login page
   - Cannot view profile

### Test Edit Profile

#### Test Case 1: Update Profile Information
1. Login to the application
2. Navigate to `http://localhost:8000/blog/edit_profile/`
3. Update fields:
   - Change email
   - Update first name and last name
4. Click "Update Profile"
5. **Expected Result**: 
   - Profile is updated
   - Redirected to profile page
   - Changes are visible

#### Test Case 2: Upload Profile Picture
1. Navigate to edit profile page
2. Select an image file
3. Click "Update Profile"
4. **Expected Result**: 
   - Image is uploaded
   - Image is resized to 300x300 (if larger)
   - Image is displayed on profile page

#### Test Case 3: Update Profile with Invalid Data
1. Navigate to edit profile page
2. Enter invalid email format
3. Click "Update Profile"
4. **Expected Result**: 
   - Form displays validation errors
   - Profile is not updated
   - User can correct and resubmit

### Test Profile Picture Resizing

#### Test Case 1: Large Image Upload
1. Prepare an image larger than 300x300 pixels
2. Upload via edit profile page
3. **Expected Result**: 
   - Image is automatically resized to 300x300
   - Original aspect ratio maintained (thumbnail)
   - Image is saved

#### Test Case 2: Small Image Upload
1. Prepare an image smaller than 300x300 pixels
2. Upload via edit profile page
3. **Expected Result**: 
   - Image is saved as-is (no resizing needed)
   - Original size maintained

### Integration Testing

#### Test Case 1: Complete User Journey
1. Register new user
2. Login with new credentials
3. View profile
4. Edit profile (update information and upload picture)
5. Logout
6. Login again
7. Verify profile changes persisted
8. **Expected Result**: 
   - All steps complete successfully
   - Data persists across sessions

#### Test Case 2: Password Reset Flow
1. Register and login
2. Logout
3. Request password reset
4. Complete password reset via email link
5. Login with new password
6. **Expected Result**: 
   - Password reset works end-to-end
   - Can login with new password
   - Old password no longer works

---

## Technical Implementation

### Database Configuration
- **Database**: MySQL
- **Database Name**: `blog_db` (configurable in settings.py)
- **Auto-creation**: Database is automatically created on first run (via `blog/apps.py`)

### Authentication Backend
- Uses Django's default authentication backend
- Session-based authentication
- Password hashing: PBKDF2 (Django default)

### Security Features
- CSRF protection on all forms
- Password hashing (never stored in plain text)
- Session management
- Secure password reset tokens
- Login required decorators for protected views

### File Uploads
- Profile pictures stored in `media/profile_pictures/`
- Image processing using PIL/Pillow
- Automatic image resizing
- File size limits (Django default)

### URL Patterns
All authentication URLs are under `/blog/` prefix:
- Registration: `/blog/register/`
- Login: `/blog/login/`
- Logout: `/blog/logout/`
- Password Reset: `/blog/password_reset/` and related URLs
- Profile: `/blog/profile/`
- Edit Profile: `/blog/edit_profile/`

### Templates
All templates are located in `blog/templates/blog/`:
- `login.html` - Login form
- `logout.html` - Logout confirmation
- `register.html` - Registration form
- `profile.html` - User profile display
- `edit_profile.html` - Profile editing form
- Password reset templates (if custom)

### Signals
- `post_save` signal on User model
- Automatically creates Profile when User is created
- Located in `blog/models.py`

### Dependencies
- Django 6.0.1+
- MySQL client library (`mysqlclient`)
- PIL/Pillow (for image processing)
- Python 3.x

---

## Troubleshooting

### Common Issues

#### Issue: Cannot login after registration
**Solution**: Verify user was created in database. Check password hashing is working.

#### Issue: Profile picture not displaying
**Solution**: 
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings.py
- Verify file was uploaded to correct directory
- Check file permissions

#### Issue: Password reset email not sending
**Solution**: 
- Configure email backend in settings.py
- For development, use console email backend
- Check email server configuration for production

#### Issue: "Method Not Allowed" on logout
**Solution**: Verify `http_method_names=['get', 'post']` is set in LogoutView configuration.

#### Issue: Profile not created automatically
**Solution**: 
- Check signal is properly registered
- Verify migrations are applied
- Check database for Profile records

---

## Conclusion

This authentication system provides a complete, secure, and user-friendly authentication experience using Django's built-in authentication framework. All features are fully functional and tested, with custom templates providing a consistent user interface.

For additional information, refer to:
- [Django Authentication Documentation](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django User Authentication](https://docs.djangoproject.com/en/stable/topics/auth/default/)
