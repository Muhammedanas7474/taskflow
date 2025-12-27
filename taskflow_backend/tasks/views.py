from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from .permissions import is_manager, is_developer
from django.shortcuts import get_object_or_404


class TaskListCreateAPIView(APIView):

    def get(self, request):
        user = request.user

        if is_manager(user):
            tasks = Task.objects.all()
            
            status_q = request.query_params.get('status')
            assignee_q = request.query_params.get('assignee')

            if status_q:
                tasks = tasks.filter(status=status_q)
            if assignee_q:
                tasks = tasks.filter(assignee_id=assignee_q)
        else:
            tasks = Task.objects.filter(assignee=user)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data.copy()

        if is_developer(user):
            data['assignee'] = user.id

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class TaskDetailAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self, request, pk):
        task = self.get_object(pk)
        user = request.user

        if is_developer(user) and task.assignee != user:
            return Response({"detail": "Not allowed"}, status=403)

        return Response(TaskSerializer(task).data)

    def put(self, request, pk):
        task = self.get_object(pk)
        user = request.user

        if is_developer(user):
            if task.assignee != user:
                return Response({"detail": "Not allowed"}, status=403)
            
            data = {'status': request.data.get('status', task.status)}
        else:
            data = request.data

        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = request.user
        if not is_manager(user):
            return Response({"detail": "Only managers can delete"}, status=403)

        task = self.get_object(pk)
        task.delete()
        return Response(status=204)
