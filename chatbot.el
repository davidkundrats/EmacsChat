;;-*- lexical-binding: t -*-
;;; chat-with-bot.el --- Chat with a Flask app from Emacs

;; Author: David Kundrats
;; Version: 1.0
;; Description: Interactive chat with an RAG chatbot via Flask app using a dedicated Emacs buffer.

(require 'request)

(global-set-key (kbd "C-c c") 'start-chat)
(global-set-key (kbd "C-c s") 'send-message-to-chat)

(defun start-chat ()
  "Starts a chat session with the Flask app."
  (interactive)
  (start-flask-app)
  (sleep-for 2) ;; TODO: change this to polling
  
  )

(defun chat-process-filter (process output)
   (let ((chat-buffer (process-buffer process)))
    (if (buffer-live-p chat-buffer)
        (with-current-buffer chat-buffer
          (goto-char (point-max))
          (insert output))
      (delete-process process))))

(defun send-message-to-chat ()
  "Send a message to the Flask chat app."
  (interactive)
  (let ((user-input (read-from-minibuffer "Send message: ")))
    (request
     "http://127.0.0.1:5000/chat"
     :type "POST"
     :headers '(("Content-Type" . "application/json"))
     :data (json-encode `(("message" . ,user-input)))
     :parser 'json-read
     :success (cl-function
               (lambda (&key data &allow-other-keys)
                 (let ((response-buffer (get-buffer-create "*Chat Response*")))
                   (with-current-buffer response-buffer
                     (goto-char (point-max))
                     ;; Display the request
                     (insert (format "Request: %s\n" user-input)) 
                     ;; Display the response
                     (insert (format "Response: %s\n" (assoc-default 'response data)))
                     (display-buffer response-buffer)))))
     :error (cl-function
             (lambda (&rest args &key error-thrown &allow-other-keys)
               (message "Failed to send message: %S" error-thrown))))))

(defun start-flask-app ()
  "Starts the Flask app."
  (interactive)
  (let ((flask-process (start-process "flask-app" "*FlaskApp*" "/home/david/Projects/Python/EmacChat/venv/bin/python" "./app.py")))
    (set-process-filter flask-process
                        (lambda (process output)
                          (when (string-match "Running on http://127.0.0.1:5000/" output)
                            (message "Flask app started successfully.")))))
  (message "Starting Flask app..."))

