

%rebase layout_skonf globals(), title="Host %s" % elt.get('host_name', 'unknown'),  css=['elements/css/token-input.css', 'elements/css/token-input-facebook.css', 'elements/css/jquery.bsmselect.css', 'elements/css/jquery-ui.css'], js=['elements/js/host.js', 'elements/js/jquery.tokeninput.js', 'elements/js/jquery.bsmselect.js', 'elements/js/jquery.bsmselect.sortable.js', 'elements/js/jquery.bsmselect.compatibility.js', 'elements/js/sliders.js', 'elements/js/selects.js', 'elements/js/forms.js']

<script>

// Keep a list of all properties, with their own properties :)
var properties = [];

    </script>

</script>

<div class='offset1 span10'>
  <span id='saving_log' class='hide alert'></span>
</div>

<a class='btn btn-info' href="javascript:submit_form()"><i class="icon-ok"></i> Submit</a>

<div class='offset1 span10'>
  <form name='form-host'>
    <input name="_id" type="hidden" value="{{elt.get('_id', '')}}"/>
    <ul class="nav nav-tabs">
      <li class="active"><a href="#generic" data-toggle="tab">Generic</a></li>
      <li><a href="#direct" data-toggle="tab">Direct configuration</a></li>
      <li><a href="#macros" data-toggle="tab">Macros</a></li>
    </ul>
    
    <div class="tab-content">
      <!-- Tab Generic Stop-->
      <div class="tab-pane active" id="generic">

	{{!helper.get_string_input(elt, 'contact_name', 'Contact name', span='span5', popover='Name of the contact. Should be unique.')}}
	{{!helper.get_string_input(elt, 'display_name', 'Display name', span='span6', innerspan='span3', placeholder=elt.get('contact_name', ''))}}
	{{!helper.get_string_input(elt, 'email', 'Email', span='span5')}}
	{{!helper.get_string_input(elt, 'pager', 'Phone', span='span5')}}
	<span class="span10">
	  <span class="help-inline span1">Tags </span>
	  <input id='use' class='to_use_complete offset1' data-use='{{elt.get('use', '')}}' data-cls='contact' name="use" type="text" tabindex="2"/>
	  <script>properties.push({'name' : 'use', 'type' : 'use_tags'});</script>
	</span>
	{{!helper.get_bool_input(elt, 'can_submit_commands', 'Can submit command')}}
	{{!helper.get_bool_input(elt, 'is_admin', 'Is a monitoring administrator')}}
	
      </div>
      <!-- Tab Generic stop-->


      <!-- Tab Macros -->
      <div class="tab-pane" id="direct">
	{{!helper.get_select_input(elt, 'host_notification_period', 'Host notification Period', 'timeperiods', 'timeperiod_name')}}
	{{!helper.get_select_input(elt, 'service_notification_period', 'Service notification Period', 'timeperiods', 'timeperiod_name')}}


	{{!helper.get_bool_input(elt, 'host_notifications_enabled', 'Enable host notifications')}}	
	{{!helper.get_bool_input(elt, 'service_notifications_enabled', 'Enable service notifications')}}	

	{{!helper.get_multiselect_input(elt, 'host_notification_commands', 'Host notification commands', 'commands', 'command_name')}}
	{{!helper.get_multiselect_input(elt, 'service_notification_commands', 'Service notification commands', 'commands', 'command_name')}}

	{{!helper.get_string_input(elt, 'host_notification_options', 'Host notification options')}}
	{{!helper.get_string_input(elt, 'service_notification_options', 'Service notification options')}}

	{{!helper.get_string_input(elt, 'min_business_impact', 'Minimum business impact (filter)')}}


      </div>
      <!-- Tab Macros stop -->


      <!-- Tab Macros -->
      <div class="tab-pane" id="macros">
	None
      </div>
      <!-- Tab Macros stop -->




    </div>

    
    
    <!--{{elt}} -->

  </form>

</div>
