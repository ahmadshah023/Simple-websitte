from django.shortcuts import render, redirect
import pandas as pd


def project(request):
    return render(request, 'project.html')


def data_analysis(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            file_name = uploaded_file.name

            if file_name.endswith('.csv'):
                dataFrame = pd.read_csv(uploaded_file)
                request.session['file_type'] = 'csv'
                request.session['file_name'] = file_name
                request.session['num_rows'], request.session['num_columns'] = dataFrame.shape
                request.session['column_names'] = dataFrame.columns.tolist()
                request.session['error_message'] = None
            elif file_name.endswith('.txt'):
                content = uploaded_file.read().decode('utf-8')
                request.session['file_type'] = 'txt'
                request.session['file_name'] = file_name
                request.session['file_content'] = content
                request.session['error_message'] = None

            else:
                # Handle unsupported file types
                request.session['file_type'] = 'unsupported'
                request.session['file_name'] = file_name
                request.session['error_message'] = 'This type of file is not supported'
            return redirect('success')
        else:
            request.session['file_name'] = 'None'
            request.session['error_message'] = 'Please choose a file to upload'
            return redirect('success')


    else:
        return render(request, 'da.html')


def success(request):
    file_type = request.session.get('file_type')
    file_name = request.session.get('file_name')
    error_message = request.session.get('error_message')

    context = {
        'file_type': file_type,
        'file_name': file_name,
        'error_message': error_message
    }

    if file_type == 'csv':
        context.update({
            'num_rows': request.session.get('num_rows'),
            'num_columns': request.session.get('num_columns'),
            'column_names': request.session.get('column_names')
        })
    elif file_type == 'txt':
        context.update({
            'file_content': request.session.get('file_content')
        })

    return render(request, 'success.html', context)


