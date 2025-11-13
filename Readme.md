# Fusion Exporter Add-In

Restore multi-format export functionality in Fusion 360 Personal Edition. This add-in enables clean export to **STL**, **STEP**, **IGES**, and **3MF** using a dropdown UI and folder picker—no more manual workarounds.

## 🔧 Features

- Export active design to STL, STEP, IGES, or 3MF
- Dropdown format selector (no typing required)
- Folder picker for export destination
- UI-integrated button under **Tools > Add-Ins**
- Compatible with Fusion 360 Personal Edition (Windows & Mac)

## 📦 Installation

1. Download or clone this repository
2. Copy the folder to:
%AppData%\Autodesk\Autodesk Fusion 360\API\AddIns\


On macOS, use:
~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/
3. Launch Fusion 360
4. Go to **Tools > Scripts and Add-Ins > Add-Ins tab**
5. Select `Fusion_Exporter_Addin` and click **Run**
6. Use the new **Fusion Exporter** button in the toolbar

## 🧠 Notes

- Exports use the root component name for filenames
- Format selection is case-safe via dropdown
- Works around export restrictions in Fusion Personal Edition
- Modular structure for future expansion (DXF, batch export, etc.)

## 📸 Screenshots

Use the images folder



## 🛠️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Pull requests welcome! If you’d like to add DXF support, batch export, or slicer integration, feel free to fork and extend.

## 📣 Credits


Created by **Ric** to restore real-world usability for makers using Fusion 360.
