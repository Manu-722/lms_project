from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer
from rest_framework.permissions import IsAuthenticated
from .forms import SubmissionForm
from django.utils import timezone




# Create your views here.
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

# Template view for submitting assignments
def submit_assignment_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if timezone.now() > assignment.due_date:
        return render(request, 'submit_assignment.html', {
            'assignment': assignment,
            'error': 'Deadline has passed. Submission is closed.'
        })

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('course_list')
    else:
        form = SubmissionForm()

    return render(request, 'submit_assignment.html', {
        'assignment': assignment,
        'form': form
    })
