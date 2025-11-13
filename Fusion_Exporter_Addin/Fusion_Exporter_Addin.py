import adsk.core, adsk.fusion, traceback, os

handlers = []

def run(context):
    try:
        create_ui_button()
    except:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Add-in failed:\n{}'.format(traceback.format_exc()))

def create_ui_button():
    app = adsk.core.Application.get()
    ui = app.userInterface

    cmd_definitions = ui.commandDefinitions
    cmd_id = 'FusionExporterDropdown'

    if cmd_definitions.itemById(cmd_id):
        return

    cmd_def = cmd_definitions.addButtonDefinition(
        cmd_id,
        'Fusion Exporter',
        'Export active design to STL, STEP, IGES, or 3MF',
        ''
    )

    tools_panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
    if tools_panel:
        tools_panel.controls.addCommand(cmd_def)

    on_command_created = CommandCreatedHandler()
    cmd_def.commandCreated.add(on_command_created)
    handlers.append(on_command_created)

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        try:
            cmd = args.command
            inputs = cmd.commandInputs

            # Add dropdown input
            dropdown_input = inputs.addDropDownCommandInput(
                'formatDropdown',
                'Export Format',
                adsk.core.DropDownStyles.TextListDropDownStyle
            )
            dropdown_input.listItems.add('STL', True)
            dropdown_input.listItems.add('STEP', False)
            dropdown_input.listItems.add('IGES', False)
            dropdown_input.listItems.add('3MF', False)

            # Attach execute handler
            on_execute = CommandExecuteHandler()
            cmd.execute.add(on_execute)
            handlers.append(on_execute)

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Command creation failed:\n{}'.format(traceback.format_exc()))

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            inputs = args.command.commandInputs

            format_input = inputs.itemById('formatDropdown')
            selected_format = None
            for item in format_input.listItems:
                if item.isSelected:
                    selected_format = item.name
                    break

            if not selected_format:
                ui.messageBox("No format selected. Exiting.")
                return

            # Folder picker
            folder_dialog = ui.createFolderDialog()
            folder_dialog.title = 'Select export destination'
            if folder_dialog.showDialog() != adsk.core.DialogResults.DialogOK:
                ui.messageBox('Export cancelled.')
                return
            export_path = folder_dialog.folder

            export_selected_component(selected_format, export_path)

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Export failed:\n{}'.format(traceback.format_exc()))

def export_selected_component(format, folder):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct

    if not isinstance(design, adsk.fusion.Design):
        ui.messageBox('No active Fusion design.')
        return

    root = design.rootComponent
    export_mgr = design.exportManager
    filename = os.path.join(folder, f"{root.name}.{format.lower()}")

    try:
        if format == 'STL':
            stl_options = export_mgr.createSTLExportOptions(root)
            stl_options.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            stl_options.filename = filename
            export_mgr.execute(stl_options)

        elif format == 'STEP':
            step_options = export_mgr.createSTEPExportOptions(filename)
            export_mgr.execute(step_options)

        elif format == 'IGES':
            iges_options = export_mgr.createIGESExportOptions(filename)
            export_mgr.execute(iges_options)

        elif format == '3MF':
            mf_options = export_mgr.create3MFExportOptions(root)
            mf_options.filename = filename
            export_mgr.execute(mf_options)

        ui.messageBox(f"Exported {format} to:\n{filename}")

    except Exception as e:
        ui.messageBox(f"Export failed:\n{e}")