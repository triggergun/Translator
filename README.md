# Translator
**A simple locale translation tool at your service.**

### Backstory
 In my quest of *4000 Essential Words* , I grappled with unfamiliar terms that were hard to comprehend and summarize. Hence, the idea for this app blossomed.
 I recallimg the torturous dictionary loading phase but today, everything's smooth sailing: correcting errors, batch processing, even printing them out. A notable enhancement indeed!
 Along the way, countless words swimming around in my head——more than 300, to be precise. Thanks for sticking with me these past few months! And also supports from community.

### How to Use
 This project is mainly using PySide6 to create user interface.
 It primarily uses the local dictionary for English-Chinese translation, focusing on word translation, saving, and printing.
 For Chinese-English translation or online mode, we rely on Google Online Translate and Cloudfare (currently inaccessible in China).
 Translation prioritizes current document words, with different background colors for offline/online translations.
 Automatic saving off? Closing the program discards unsaved files. Remember to hit 'Save' often!
 Settings file is located at **%25 AppData\settings.tsf**. Delete to revert to defaults.
 Files are stored using pickle and zlib compression, with TVF (word book file) supporting parameter transfer startup and single-instance operation.
 A handful of sample plugins reside in the tools folder. The plugin system is comprehensive, allowing for Python files recognized by importlib to be loaded.

### Functions

 - Base translate / correct function \
  ![Translate](https://github.com/user-attachments/assets/e540593d-605f-4974-a0fa-a2402e8d6bb1 "Translate")
  ![Correct](https://github.com/user-attachments/assets/3c52cfbd-f210-424b-b793-e94e2db5e09b "Correct")

 - Generate documents (using `python-docx` lib) \
  ![Document](https://github.com/user-attachments/assets/dd0622d1-3c51-449f-99a3-01ba13d96a52)

 - Import / Export \
  ![Export](https://github.com/user-attachments/assets/fba753d0-3ef9-4f78-b4b6-f67689c1cc51)

 - Google Translate  
    <img src="https://github.com/user-attachments/assets/d5203c03-a609-4be8-9ab8-30d354032ecd" width="555" height="388">

 - Dictionaries management  
    <img src="https://github.com/user-attachments/assets/57c61cc0-972b-40e3-bb1e-2c6709a262c4" width="555" height="388">

 - Setting / MultiLanguage  
    <img src="https://github.com/user-attachments/assets/e372e2b4-a1e0-465d-83fe-e127905dd752" width="555" height="388">
    <img src="https://github.com/user-attachments/assets/82938db9-cf5e-4932-893a-8f9bca94a6f5" width="555" height="388">

 - File operation \
  ![File Operation](https://github.com/user-attachments/assets/e6b2e23a-de22-43b6-a365-5f1cb9c93a01)
