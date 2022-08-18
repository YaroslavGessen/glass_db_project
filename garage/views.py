import openpyxl_dictreader
import os
from django.conf import settings
from django.http import Http404, FileResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from plotly.offline import plot
import plotly.graph_objects as go

from garage.models import Vehicles, Glasses, Vectors
from garage.forms import VehicleForm, GlassForm, UserRegistrationForm, UserLoginForm


def redirect_to_login_view(request):
    response = redirect('/login')
    return response


def index(request):
    cars = Vehicles.objects.all()
    return render(request, 'garage/show.html', {"cars": cars})


def add_new_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VehicleForm()
    return render(request, 'garage/index.html', {'form': form})


def edit_vehicle(request, id):
    vehicle = Vehicles.objects.get(id=id)
    return render(request, 'garage/edit_vehicle.html', {'vehicle': vehicle})


def update_vehicle(request, id):
    vehicle = Vehicles.objects.get(id=id)
    form = VehicleForm(request.POST, instance=vehicle)
    if form.is_valid():
        form.save()
        return redirect('home')
    else:
        return render(request, 'garage/edit_vehicle.html', {'vehicle': vehicle, 'form': form})


def destroy_vehicle(request, id):
    vehicle = Vehicles.objects.get(id=id)
    vehicle.delete()
    return redirect('home')


def glasses(requset, id):
    glass = Glasses.objects.filter(g_model_id=id)
    model_id = id
    return render(requset, 'garage/show_glass.html', {'glasses': glass, 'modelid': model_id})


def add_new_glass(request, id):
    if request.method == "POST":
        form = GlassForm(request.POST, initial={'g_model': id})
        if form.is_valid():
            form.save()
            return redirect(f'/glasses/{id}')
    else:
        form = GlassForm(initial={'g_model': id})
        return render(request, 'garage/add_glass.html', {'form': form, 'modelid': id})


def edit_glass(request, id):
    glass = Glasses.objects.get(id=id)
    return render(request, 'garage/edit_glass.html', {'glass': glass})


def update_glass(request, id):
    glass = Glasses.objects.get(id=id)
    model_id = glass.g_model_id
    form = GlassForm(request.POST, instance=glass)
    if form.is_valid():
        form.save()
        return redirect(f'/glasses/{model_id}')
    else:
        return render(request, 'garage/edit_glass.html', {'glass': glass, 'form': form})


def vehicle_details(request, source):
    try:
        if Vectors.objects.filter(v_source=source).exists():
            vector = Vectors.objects.get(v_source=source)
            car_vector = vector.json_data
            projects_data = [i for i, _ in enumerate(car_vector['values'])]
            graphs = []
            graphs.append(
                go.Scatter(x=projects_data, y=car_vector['values'], mode='markers')
            )
            layout = {
                'title': f'Scatter Plot of file {source}',
                'xaxis_title': 'Index',
                'yaxis_title': 'Vectors',
                'height': 420,
                'width': 1024,
            }
            # Getting HTML needed to render the plot.
            plot_div = plot({'data': graphs, 'layout': layout},
                            output_type='div')
            return render(request, 'garage/vehicle_details.html', {'vector': vector, 'plot_div': plot_div})
        else:
            messages.warning(request, f'Vector with source {source} not found')
            return redirect(f'/')
    except Exception as e:
        messages.warning(request, f'Vector do not exists.\n Error message: {e}')
        return redirect(f'/')


def destroy_glass(request, id):
    glass = Glasses.objects.get(id=id)
    model_id = glass.g_model_id
    glass.delete()
    return redirect(f'/glasses/{model_id}')


def destroy_vector(request, id):
    vector = Vectors.objects.get(id=id)
    vector.delete()
    return redirect(f'show_vectors')


def vectors(request):
    vectors_data = Vectors.objects.all()
    return render(request, 'garage/show_vectors.html', {"vectors": vectors_data})


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def login_func(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user or None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Username or password is wrong')
            return redirect('login')
    else:
        user_form = UserLoginForm()

    return render(request, 'registration/login.html', {'user_form': user_form})


def logout_func(request):
    logout(request)
    return redirect("/")


def import_to_vehicles(request):
    if request.method == 'POST':
        try:
            xls_file = request.FILES['vehicle_file']
            json_data = {}
            reader = openpyxl_dictreader.DictReader(xls_file)
            for rows in reader:
                for row_id, row_value in rows.items():
                    json_data[row_id] = row_value

                # Check if car exists in laboratory, if not create object
                if Vehicles.objects.filter(v_number=json_data['plate number']).exists():
                    pass
                else:
                    vehicle_to_save = Vehicles.objects.create(v_number=json_data['plate number'],
                                                              v_manufacture=json_data['model'],
                                                              v_date_of_prod=json_data['date_of_prod'])
                    vehicle_to_save.save()

                if json_data['plate number'] is None:
                    messages.warning(request, f'Plate number is empty in row: {rows}')
                    pass
                else:
                    vehicle = Vehicles.objects.get(v_number=json_data['plate number'])
                    vehicle_id = vehicle.id

                    galss_to_save = Glasses.objects.create(g_damage_type=json_data['type'],
                                                           g_damage_side=json_data['side'],
                                                           g_source=json_data['file'],
                                                           g_nak=json_data['NaK'],
                                                           g_mgk=json_data['MgK'],
                                                           g_alk=json_data['AlK'],
                                                           g_sik=json_data['SiK'],
                                                           g_sk=json_data['S K'],
                                                           g_cik=json_data['ClK'],
                                                           g_kka=json_data['K KA'],
                                                           g_kkb=json_data['K KB'],
                                                           g_caka=json_data['CaKA'],
                                                           g_cakb=json_data['CaKB'],
                                                           g_tik=json_data['TiK'],
                                                           g_crk=json_data['CrK'],
                                                           g_mnk=json_data['MnK'],
                                                           g_fek=json_data['FeK'],
                                                           g_coka=json_data['CoKA'],
                                                           g_cuka=json_data['CuKA'],
                                                           g_cukb=json_data['CuKB'],
                                                           g_znka=json_data['ZnKA'],
                                                           g_znkb=json_data['ZnKB'],
                                                           g_srk=json_data['SrK'],
                                                           g_model_id=vehicle_id)
                    galss_to_save.save()
            messages.success(request, 'File was added successfully!')
            return redirect('/')
        except Exception as e:
            messages.warning(request, f'Something went wrong during upload! '
                                      f'Error:  {e}')
            return redirect('/')

    return redirect('/')


def import_vector(request):
    if request.method == 'POST':
        try:
            xls_file = request.FILES['vector_file']
            json_vector = {'values': []}
            json_values = {}
            reader = openpyxl_dictreader.DictReader(xls_file)
            for rows in reader:
                json_vector['values'].clear()
                for row_id, row_value in rows.items():
                    if isinstance(row_id, int):
                        json_vector['values'].append(row_value)
                    else:
                        json_vector[row_id] = row_value

                json_values['values'] = json_vector['values']
                if Vectors.objects.filter(v_source=json_vector['file_source']).exists():
                    vector = Vectors.objects.get(v_source=json_vector['file_source'])
                    vector.json_data = json_values
                    messages.warning(request, f'This file source already exists: {json_vector["file_source"]}\n'
                                              f'Updating data')
                else:
                    vector = Vectors.objects.create(v_source=json_vector["file_source"],
                                                   json_data=json_values)
                vector.save()
        except:
            messages.warning(request, f'Wrong or empty file! Please use example template')
            return redirect(f'/')
        messages.success(request, 'Vectors was added successfully!')
        return redirect(f'/')


@login_required
def download_file(request, file_path):
    # Define Django project base directory
    filepath = os.path.join(settings.MEDIA_ROOT, file_path)
    try:
        response = FileResponse(open(filepath, 'rb'), content_type='.xlsx')
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404
