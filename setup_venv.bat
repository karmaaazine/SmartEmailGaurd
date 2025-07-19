@echo off
echo 🛡️ Smart Email Guardian - Virtual Environment Setup
echo ==================================================

echo.
echo 📦 Creating virtual environment...
python -m venv venv

echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To run the application:
echo.
echo Terminal 1 - Backend:
echo   call venv\Scripts\activate.bat
echo   cd backend
echo   python app_simple.py
echo.
echo Terminal 2 - Frontend:
echo   call venv\Scripts\activate.bat
echo   cd frontend
echo   streamlit run app.py
echo.
echo Terminal 3 - Gmail Integration:
echo   call venv\Scripts\activate.bat
echo   cd gmail_integration
echo   python gmail_reader.py
echo.
echo 🌐 Access the application at:
echo   Frontend: http://localhost:8501
echo   Backend: http://localhost:8000
echo.
pause 