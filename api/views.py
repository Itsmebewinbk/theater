from rest_framework import generics,permissions,status
from rest_framework.response import Response
from Customer.models import BookingRequest
from Admin.models import CustomUser
from Theater.models import Theater,Screen,Movie,Show
from api.serializer import (UserRegistrationSerializer,
TheaterRegistrationSerializer,
                            TheaterSerializer,ScreenSerializer,SpecificScreenSerializer,
                            MovieSerializer,ShowSerializer,DeleteMovieSerializer,MovieListSerializer,
                            MovieDetailSerializer,ShowdateSerializer,BookingSerializer,BookingListSerializer,
                            AdminApprovalSerialzier)

from api.permissions import THeatreAuthentication,CustomerAuthentication,AdminAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset=CustomUser.objects.all()
   

class TheaterRegistrationView(generics.CreateAPIView):
    serializer_class = TheaterRegistrationSerializer
    queryset=CustomUser.objects.all()
    

class AddListTheaterView(generics.ListCreateAPIView):
    queryset=Theater.objects.all()
    serializer_class=TheaterSerializer
    permission_classes=(THeatreAuthentication,)
    filter_backends=[SearchFilter]
    search_fields=["city","theater_name"]

    def get_queryset(self,**kwargs):
        return Theater.objects.filter(owner=self.request.user)



class TheaterView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Theater.objects.all()
    serializer_class=TheaterSerializer
    lookup_field="id"
    permission_classes=(THeatreAuthentication,)

    def get_queryset(self,**kwargs):
        return Theater.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.theater_status = "inactive"
        instance.save()

    

#theater/<int:id>/screen
class ScreenView(generics.ListCreateAPIView):
    queryset=Screen.objects.all()
    lookup_url_kwarg="id"
    serializer_class=ScreenSerializer
    permission_classes=(THeatreAuthentication,)

    def get_queryset(self,**kwargs):
        return Screen.objects.filter(theater__owner=self.request.user,theater__id=self.kwargs[self.lookup_url_kwarg])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request,"theater_id":self.kwargs[self.lookup_url_kwarg]})
        return context

    # def create(self, request, *args, **kwargs):
    #     serializer=self.serializer_class(data=request.data,context={'request':request,
    #     "theater_id":self.kwargs[self.lookup_url_kwarg]})
    #     if serializer.is_valid(raise_exception=True):
    #             serializer.save()
    #     return Response(data=serializer.data,status=status.HTTP_201_CREATED) 
    
class SpecificScreenView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Screen.objects.all()
    serializer_class=SpecificScreenSerializer
    permission_classes=(THeatreAuthentication,)
    lookup_field=("id")

    def get_queryset(self,*args,**kwargs):
        return Screen.objects.filter(theater__owner=self.request.user)


class MovieView(generics.ListCreateAPIView):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    permission_classes=(THeatreAuthentication,)
    lookup_url_kwarg="id"

    def get_queryset(self,**kwargs):
        return Movie.objects.filter(screen__theater__owner=self.request.user,screen__id=self.kwargs[self.lookup_url_kwarg])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request,"screen_id":self.kwargs[self.lookup_url_kwarg]})
        return context

class DeleteMovieView(generics.DestroyAPIView):
    queryset=Movie.objects.all()
    serializer_class=DeleteMovieSerializer
    permission_classes=(THeatreAuthentication,)
    lookup_field="id"
    
    def get_queryset(self,*args,**kwargs):
        return Movie.objects.filter(screen__theater__owner=self.request.user)

class ShowView(generics.ListAPIView):
    queryset=Show.objects.all()
    serializer_class=ShowSerializer
    permission_classes=(THeatreAuthentication,)
    lookup_url_kwarg="id"

    def get_queryset(self,**kwargs):
        return Show.objects.filter(movie__screen__theater__owner=self.request.user,movie__id=self.kwargs[self.lookup_url_kwarg])

class DeleteShowView(generics.DestroyAPIView):
    queryset=Show.objects.all()
    serializer_class=ShowSerializer
    permission_classes=(THeatreAuthentication,)
    lookup_field="id"
    
    def get_queryset(self,*args,**kwargs):
        return Show.objects.filter(movie__screen__theater__owner=self.request.user)

    def perform_destroy(self, instance):
        instance.screen_status= "cancelled"
        instance.save()

class MovieListView(generics.ListAPIView):
    queryset=Movie.objects.all()
    serializer_class=MovieListSerializer
    permission_classes=(CustomerAuthentication,)


class MovieDetailView(generics.RetrieveAPIView):
    queryset=Movie.objects.all()
    serializer_class=MovieDetailSerializer
    permission_classes=(CustomerAuthentication,)
    lookup_field="pk"

class ShowDateView(generics.ListAPIView):
    queryset=Show.objects.all()
    serializer_class=ShowdateSerializer
    permission_classes=(CustomerAuthentication,)
    lookup_url_kwarg="pk"

    def get_queryset(self,**kwargs):
        return Show.objects.filter(movie__id=self.kwargs[self.lookup_url_kwarg])

class BookingView(generics.CreateAPIView):
    queryset=BookingRequest.objects.all()
    serializer_class=BookingSerializer
    permission_classes=(CustomerAuthentication,)
    lookup_url_kwarg="pk"

   

    def get_queryset(self,**kwargs):
        return BookingRequest.objects.filter(show_id=self.kwargs[self.lookup_url_kwarg],customer=self.request.user)

    def get_serializer_context(self):
        context={'request':self.request,'show_id':self.kwargs.get(self.lookup_url_kwarg)}
        return context

class BookingListView(generics.ListAPIView):
    queryset=BookingRequest.objects.all()
    serializer_class=BookingListSerializer
    permission_classes=(CustomerAuthentication,)

    def get_queryset(self,**kwargs):
        return BookingRequest.objects.filter(customer=self.request.user)


class BookingCancellView(generics.DestroyAPIView):
    queryset=BookingRequest.objects.all()
    serializer_class=BookingListSerializer
    permission_classes=(CustomerAuthentication,)
    lookup_field="id"

    def get_queryset(self,**kwargs):
        return BookingRequest.objects.filter(customer=self.request.user)

    def perform_destroy(self, instance):
        if instance.delete():
            for show in Show.objects.filter(bookingrequest__id=instance.id):
                outcome=show.TotalBooking-instance.occupancy
                show.TotalBooking=show.TotalBooking-instance.occupancy
                if  outcome == 0:
                    show.screen_status = "empty"
                    show.save()
                elif outcome - 1 >= show.movie.screen.total_seats // 2:
                    show.screen_status = "almostfull"
                    show.save()
                elif outcome > 0:
                    show.screen_status = "filling"
                    show.save()
        return show

class AdminApprovalList(generics.ListAPIView):
    queryset=Theater.objects.all()
    serializer_class=AdminApprovalSerialzier
    permission_classes=(AdminAuthentication,)

    def get_queryset(self,**kwargs):
        return Theater.objects.filter(approval=False)
  


class AdminApproval(generics.RetrieveUpdateAPIView):
    queryset=Theater.objects.all()
    serializer_class=AdminApprovalSerialzier
    permission_classes=(AdminAuthentication,)
    lookup_field='id'

    def get_queryset(self,**kwargs):
        return Theater.objects.filter(approval=False)



  

    




      


    













    
    
   
   
    
    


        

                    
                            
                        


