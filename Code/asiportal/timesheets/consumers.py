import json
from django.db.utils import IntegrityError
from django.http import QueryDict
from channels.handler import AsgiHandler
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .forms import TimeSheetEntryFormSet, TimeSheetEntryApprovalFormSet
from .models import TimeSheet, TutoringTimeSheetEntry
from django.contrib.auth.models import User
from channels import Group

# testing some stuff
@channel_session_user_from_http
def timesheet_connect(message, pk):
    # accept the connection
    try:
        timesheet = TimeSheet.objects.get(pk=pk)
    except TimeSheet.DoesNotExist:
        message.reply_channel.send({"text" : "nope", "close":True,})
        return
    message.reply_channel.send({"accept": True})
    Group(timesheet.group_name).add(message.reply_channel)

def update_timesheet_connect(message, tl_name):
    message.reply_channel.send({"accept" : True})
    Group(tl_name).add(message.reply_channel)

def update_timesheet_submit(message, tl_name):
    data = QueryDict(json.loads(message['text'])['formdata'])
    formset = TimeSheetEntryApprovalFormSet(data=data)
    if formset.is_valid():
        message.reply_channel.send({"text" : "goodforms"})
        for form in formset: 
            if form.has_changed():
                obj = form.save()
                objinfo = {
                            "id" : obj.id,
                            "verified" : obj.tl_verified,}
                message.reply_channel.send({"text" : json.dumps(objinfo)})

@channel_session_user
def timesheet_receive(message, pk):
    sheet = TimeSheet.objects.get(pk=pk)
    data = QueryDict(json.loads(message['text'])['formdata'])
    formset = TimeSheetEntryFormSet(data=data, 
            form_kwargs = {'user' : message.user,
                        'parent' : sheet,
                        })
    if formset.is_valid():
        message.reply_channel.send({"text" : "good form" })
        for form in formset:
            temp = form.save(commit=False)
            temp.timesheet = sheet
            try:
                temp.save()
            # prevent session from dying if they try to submit duplicate objects
            except IntegrityError:
                duplicate_err = {
                        'errors' : True,
                        'message' : '<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Duplicate Session Error:</strong><br \> It seems that you\'ve submitted more than one entry for : <p><strong>{}</strong></p>. One or none of your submissions may have been processed. Please refresh the page to check that the time has been successfully submitted. If it has not then please resubmit that entry again.</div>'.format(temp.session.__str__()),
                         }
                message.reply_channel.send({"text" : json.dumps(duplicate_err)})
    else:
        print(formset.non_form_errors())
        for dict in formset.errors:
            for error in dict.values():
                print(error)
        errs = {
                'errors' : True,
                'message' : '<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Uh oh</strong> There was a problem processing your entries. Check over them to make sure you have filled in all the fields. If this error persists please contact the website admin for further assitance. </div>',
                }
        message.reply_channel.send({"text" : json.dumps(errs) })

@channel_session_user
def timesheet_delete(message, pk):
    data = json.loads(message['text'])['delete']
    message.reply_channel.send({"text" : "i got your request broski"})
    try:
       ts =  TutoringTimeSheetEntry.objects.get(id=data)
    except TutoringTimeSheetEntry.DoesNotExist:
        message.reply_channel.send({"text" : "that doesnt exist my friend"})
        return
    ts.delete()
    message.reply_channel.send({"text" : "object deleted"})
