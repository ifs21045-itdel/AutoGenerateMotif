from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import save_combined_motif
from .views import ubah_warna
from .views import PostColoredMotifImage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generator/', views.image, name="generator"),
    path('Monitoring', views.loading, name="Monitoring"),
    path('home/', views.generator, name="home"),
    path('generator/external', views.external),
    path('save', views.save),
    path('gabungkan-motif/', views.gabungkan_motif, name='gabungkan_motif'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('save_combined_motif/', save_combined_motif, name='save_combined_motif'),
    path('regenerate_motif/<int:id>/', views.regenerate_motif, name='regenerate_motif'),
    path('ubah_warna/', ubah_warna, name='ubah_warna'),  # URL untuk halaman ubah warna
    path('generator/PostImage', views.PostImage),
    path('download/PostImage', views.PostImage),
    path('save_image_to_session/', views.save_image_to_session, name='save_image_to_session'),
    path('download/', views.download, name='download_page'),
    path('post', views.createpost),
    path('tes', views.tes),
    path('list', views.show, name="list1"),
    path('list/<str:id>', views.motif, name="list"),
    path('list/Nama/<str:user>', views.tagName, name="tagUser"),
    path('list/JumlahBaris/<path:jmlBaris>/', views.tagJmlBaris, name='tagJmlBaris'),
    path('list/waktu/<str:time>', views.tagWaktu, name="tagTime"),
    path('delete/', views.deleteMotif, name="delete"),
    path('update/<int:id>', views.UpdateUser, name='update'),
    path('update/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
    path('list1', views.showTest),
    path('generator/save', views.save, name='save'),
    path('help', views.help, name="help"),
    path('help/generator', views.help_generate, name="help-generator"),
    path('help/lidi', views.help_lidi, name="help-lidi"),
    path('help/search', views.help_search, name="help-search"),
    path('help/download', views.help_download, name="help-download"),
    path('search', views.Search, name="search"),
    path('', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('register/', views.SignupPage, name='signup'),
    path('generator/save', views.save, name='save'),
    path('motif/', views.motif, name='motif'),
    path('generator/PostImageGabungan', views.PostImageGabungan),
    # warnai halaman lihat motif
    # Tambahkan path untuk mengubah warna motif
    path('ubah-warna/<int:id>/', views.ubah_warna, name='ubah_warna'),
    path('ubah_warna_combined/<int:id>/', views.ubah_warna_combined, name='ubah_warna_combined'),
    path('motif_colored/preview/<int:motif_id>', views.newMotifColoredGabunganPreview, name='motif_colored_preview'),
    # Ensure the preview page retains the colored state on refresh
    path('motif_colored/preview/<int:motif_id>/refresh', views.newMotifColoredGabunganPreview, name='motif_colored_preview_refresh'),
    # path('save/', views.save_generator, name='save_generator'),
    path('gabungkan_motif/', views.gabungkan_motif, name='gabungkan_motif'),
    path('generator/', views.generator, name='generator'),
    path('colored_motif/post-image/', PostColoredMotifImage, name='post_colored_motif_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     path('generate-motif/admin/', admin.site.urls,),
#     path('generate-motif/generator', views.image, name="generator"),
#     path('generate-motif/Monitoring', views.loading, name="Monitoring"),
#     path('generate-motif/home/', views.generator, name="home"),
#     path('generate-motif/external', views.external),
#     path('generate-motif/save', views.save),
#     path('generate-motif/PostImage', views.PostImage),
#     path('generate-motif/post', views.createpost),
#     path('generate-motif/tes', views.tes),
#     path('generate-motif/list', views.show, name="list1"),
#     path('generate-motif/list/<str:id>', views.motif, name="list"),
#     path('generate-motif/list/Nama/<str:user>', views.tagName, name="tagUser"),
#     path('generate-motif/list/JumlahBaris/<str:jmlBaris>', views.tagJmlBaris, name="tagJmlBaris"),
#     path('generate-motif/list/waktu/<str:time>', views.tagWaktu, name="tagTime"),
#     path('generate-motif/delete/', views.deleteMotif, name="delete"),
#     path('generate-motif/update/<int:id>', views.UpdateUser, name='update'),
#     path('generate-motif/update/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
#     path('generate-motif/list1', views.showTest),
#     path('generate-motif/help', views.help, name="help"),
#     path('generate-motif/help/generator', views.help_generate, name="help-generator"),
#     path('generate-motif/help/lidi', views.help_lidi, name="help-lidi"),
#     path('generate-motif/help/search', views.help_search, name="help-search"),
#     path('generate-motif/help/download', views.help_download, name="help-download"),
#     path('generate-motif/search', views.Search, name="search"),
#     path('generate-motif/',views.LoginPage,name='login'),
#     path('generate-motif/logout/',views.LogoutPage,name='logout'),
#     path('generate-motif/sregister/',views.SignupPage,name='signup')
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)