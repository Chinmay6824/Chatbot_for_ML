@echo off
echo Preparing ML Chatbot files for hosting...
echo.

echo Step 1: Creating a folder for hosting...
mkdir ml_chatbot_hosting
echo.

echo Step 2: Copying necessary files...
copy index.html ml_chatbot_hosting\
copy share_ml_chatbot.html ml_chatbot_hosting\
copy netlify_guide.html ml_chatbot_hosting\
copy github_pages_guide.html ml_chatbot_hosting\
echo.

echo Step 3: Creating a README file...
echo # ML Chatbot > ml_chatbot_hosting\README.md
echo. >> ml_chatbot_hosting\README.md
echo A simple Machine Learning chatbot with knowledge of over 60 ML concepts. >> ml_chatbot_hosting\README.md
echo. >> ml_chatbot_hosting\README.md
echo ## How to Host >> ml_chatbot_hosting\README.md
echo. >> ml_chatbot_hosting\README.md
echo 1. Upload these files to a web hosting service like Netlify, GitHub Pages, or Vercel >> ml_chatbot_hosting\README.md
echo 2. Share the URL with your friends >> ml_chatbot_hosting\README.md
echo 3. They can access the chatbot with a single click! >> ml_chatbot_hosting\README.md
echo.

echo Files are ready for hosting!
echo.
echo Your files are in the 'ml_chatbot_hosting' folder.
echo You can now upload this folder to Netlify, GitHub Pages, or any other web hosting service.
echo.
echo For detailed instructions:
echo - Open netlify_guide.html for Netlify hosting instructions
echo - Open github_pages_guide.html for GitHub Pages hosting instructions
echo.

pause 