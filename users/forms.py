from __future__ import annotations

from datetime import date
import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserRegisterForm(UserCreationForm):
    """Registration form with strong validation for username and email.

    - Enforces unique, case-insensitive email
    - Normalizes username/email to a consistent format
    - Relies on Django password validators for password strength
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username: str = self.cleaned_data.get("username", "")
        normalized_username = username.strip()
        # Allow letters, numbers, underscore, dot, and hyphen only
        if not re.fullmatch(r"[A-Za-z0-9_.-]{3,150}", normalized_username):
            raise forms.ValidationError(
                "Username must be 3-150 chars and contain only letters, numbers, _ . -"
            )
        return normalized_username

    def clean_email(self):
        user_model = get_user_model()
        email: str = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("Email is required")
        # Case-insensitive uniqueness check
        if user_model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists")
        return email


class ProfileForm(forms.ModelForm):
    """Profile editor with validations for phone, avatar, and dates."""

    MAX_AVATAR_BYTES = 2 * 1024 * 1024  # 2MB

    phone_number = forms.CharField(
        required=False,
        max_length=20,
        help_text="Optional. Digits, spaces, +, -, and parentheses only.",
    )

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "bio",
            "avatar",
            "date_of_birth",
        ]

    def clean_phone_number(self):
        phone = (self.cleaned_data.get("phone_number") or "").strip()
        if not phone:
            return ""
        if not re.fullmatch(r"[0-9+()\-\s]{7,20}", phone):
            raise forms.ValidationError(
                "Enter a valid phone number (digits, spaces, +, -, parentheses)."
            )
        return phone

    def clean_bio(self):
        bio = (self.cleaned_data.get("bio") or "").strip()
        if len(bio) > 500:
            raise forms.ValidationError("Bio must be at most 500 characters long")
        return bio

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        if dob is None:
            return dob
        if dob > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future")
        if dob.year < 1900:
            raise forms.ValidationError("Date of birth year must be 1900 or later")
        return dob

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if not avatar:
            return avatar
        # Validate size
        if getattr(avatar, "size", 0) and avatar.size > self.MAX_AVATAR_BYTES:
            raise forms.ValidationError("Avatar must be 2MB or smaller")
        # Validate mime-type if available
        content_type = getattr(avatar, "content_type", "") or ""
        if content_type and not content_type.startswith("image/"):
            raise forms.ValidationError("Avatar must be an image file")
        return avatar


