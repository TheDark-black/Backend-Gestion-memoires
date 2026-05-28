from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.roles.filter(name='admin').exists()

class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return request.user.roles.filter(name='enseignant').exists()

class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return request.user.roles.filter(name='etudiant').exists()



#### Les différents permissions specifiques pour lies aux utilisateurs


class CanManageUsers(BasePermission):

    def has_permission(self, request, view):

        print("PERMISSION APPELEE")

        return (
            request.user.is_superuser
            or request.user.roles.filter(name='admin').exists()
        )

class CanCreatSubject(BasePermission):

    def has_permission(self, request, view):
        return request.user.roles.filter(name='enseignant').exists()

class CanUploadDocument(BasePermission):

    def has_permission(self, request, view):
        return request.user.roles.filter(name='etudiant').exists()

class CanGradeDefense(BasePermission):

    def has_permission(self, request, view):
        return request.user.roles.filter(name='jury').exists()