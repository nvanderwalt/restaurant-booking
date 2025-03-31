
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Count
from .models import Booking, Table, MenuItem
from .forms import BookingForm, RegisterForm, TableForm, MenuItemForm
from datetime import datetime