from django.urls import path
from .views import AddGrainView, BaseView, AddBunkerView, BunkerDetailView, DeleteBunkerView, AddTransactionView, DeleteGrainView, EditBunkerView, GrainView
urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('add-bunker/', AddBunkerView.as_view(), name='add_bunker'),
    path('bunker/<int:pk>/', BunkerDetailView.as_view(), name='bunker_detail'),
    path('delete-bunker/<int:pk>', DeleteBunkerView.as_view(), name='delete_bunker'),
    path('add-transaction-to/<int:pk>', AddTransactionView.as_view(), name='add_transaction'),
    path('grains/', GrainView.as_view(), name='grains'),
    path('delete-grain/<int:pk>', DeleteGrainView.as_view(), name='delete_grain'),
    path('add-grain/', AddGrainView.as_view(), name='add_grain'),
    path('edit-bunker/<int:pk>', EditBunkerView.as_view(), name='edit_bunker')
]