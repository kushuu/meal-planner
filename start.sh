set -e

echo "Starting Meal Planner..."
echo ""

if command -v tmux &> /dev/null; then
    echo "Using tmux to manage services..."
    
    tmux new-session -d -s mealplanner
    
    tmux rename-window -t mealplanner:0 'Database'
    tmux send-keys -t mealplanner:0 'docker-compose up' C-m
    
    tmux new-window -t mealplanner:1 -n 'Backend'
    tmux send-keys -t mealplanner:1 'cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000' C-m
    
    tmux new-window -t mealplanner:2 -n 'Frontend'
    tmux send-keys -t mealplanner:2 'cd frontend && source .venv/bin/activate && streamlit run app.py' C-m
    
    echo ""
    echo "All services started in tmux!"
    echo ""
    echo "Tmux commands:"
    echo "  Ctrl+B, then 0/1/2 - Switch between windows"
    echo "  Ctrl+B, then D     - Detach from session"
    echo "  tmux attach -t mealplanner - Reattach"
    echo "  tmux kill-session -t mealplanner - Stop all"
    echo ""
    
    sleep 2
    tmux attach-session -t mealplanner
    
else
    echo "Starting services in separate terminal windows..."
    echo ""
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && docker-compose up"'
        sleep 2
        osascript -e 'tell app "Terminal" to do script "cd '"$PWD/backend"' && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000"'
        sleep 2
        osascript -e 'tell app "Terminal" to do script "cd '"$PWD/frontend"' && source .venv/bin/activate && streamlit run app.py"'
        
    elif command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "docker-compose up; exec bash"
        sleep 2
        gnome-terminal -- bash -c "cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000; exec bash"
        sleep 2
        gnome-terminal -- bash -c "cd frontend && source .venv/bin/activate && streamlit run app.py; exec bash"
        
    else
        echo "Could not detect terminal multiplexer."
        echo ""
        echo "Please open 3 terminals manually and run:"
        echo ""
        echo "Terminal 1: docker-compose up"
        echo "Terminal 2: cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000"
        echo "Terminal 3: cd frontend && source .venv/bin/activate && streamlit run app.py"
        exit 1
    fi
    
    echo ""
    echo "Services starting in separate terminals!"
fi

echo ""
echo "Access the application at:"
echo "   Frontend: http://localhost:8501"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""