<script>
  import { onMount } from 'svelte';
  
  let messages = [];
  let newMessage = "";
  let isLoading = false;
  let currentStreamedMessage = "";
  let modelProgress = 0;
  let modelName = "";
  let isModelLoading = true;
  let pollingInterval;
  let errorMessage = "";
  let connectionAttempts = 0;
  let statusMessage = "Connecting to server...";

  async function checkModelInfo() {
    try {
      connectionAttempts++;
      statusMessage = `Attempting to connect (try ${connectionAttempts})...`;
      
      const response = await fetch('model-info');
      if (!response.ok) {
        throw new Error(`Server returned ${response.status} ${response.statusText}`);
      }
      const data = await response.json();
      
      // Clear error if request succeeds
      errorMessage = "";
      modelProgress = data.progress;
      modelName = data.model_name;
      statusMessage = `Loading model: ${modelName}`;
      
      if (modelProgress === 100) {
        clearInterval(pollingInterval);
        isModelLoading = false;
      }
    } catch (error) {
      errorMessage = `Connection failed: ${error.message}`;
      if (connectionAttempts >= 5) {
        clearInterval(pollingInterval);
        statusMessage = "Connection attempts exceeded. Please refresh the page to try again.";
      }
    }
  }

  async function sendMessage() {
    if (!newMessage.trim()) return;
    
    // Add user message
    messages = [...messages, { role: "user", content: newMessage }];
    const userMessage = newMessage;
    newMessage = "";
    isLoading = true;
    currentStreamedMessage = "";

    try {
      const response = await fetch('chat-completion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: messages
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      // Add an initial system message that we'll update
      messages = [...messages, { role: "system", content: "" }];

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }

        // Decode the incoming bytes and append to the current message
        const text = decoder.decode(value);
        currentStreamedMessage += text;
        
        // Update the last message in the messages array
        messages = messages.map((msg, index) => {
          if (index === messages.length - 1) {
            return { ...msg, content: currentStreamedMessage };
          }
          return msg;
        });
      }
    } catch (error) {
      console.error('Error sending message:', error);
      messages = [...messages, { role: "system", content: "Sorry, there was an error processing your message." }];
    } finally {
      isLoading = false;
    }
  }

  // Start polling when component mounts
  onMount(() => {
    checkModelInfo();
    pollingInterval = setInterval(checkModelInfo, 1000);
    return () => clearInterval(pollingInterval);
  });
</script>

<main>
  {#if isModelLoading}
    <div class="loading-screen">
      <div class="loading-container">
        <h2>{statusMessage}</h2>
        
        {#if errorMessage}
          <div class="error-message">
            {errorMessage}
          </div>
        {/if}
        
        {#if modelName}
          <div class="model-info">
            <div class="model-name">Model: {modelName}</div>
            <div class="progress-bar-container">
              <div class="progress-bar" style="width: {modelProgress}%"></div>
            </div>
            <div class="progress-text">{modelProgress}% complete</div>
          </div>
        {:else}
          <div class="spinner"></div>
        {/if}
        
        {#if connectionAttempts >= 5}
          <button class="retry-button" on:click={() => window.location.reload()}>
            Retry Connection
          </button>
        {/if}
      </div>
    </div>
  {:else}
    <div class="chat-container">
      <div class="header">
        <button class="clear-button" on:click={() => messages = []}>
          Clear History
        </button>
        <div class="model-info">
          Model: {modelName}
        </div>
      </div>
      <div class="messages" id="messages-container">
        {#each messages as message}
          <div class="message {message.role}">
            <div class="message-content">
              {message.content}
            </div>
          </div>
        {/each}
        {#if isLoading && currentStreamedMessage === ""}
          <div class="message system">
            <div class="message-content loading">
              Thinking...
            </div>
          </div>
        {/if}
      </div>
      
      <div class="input-area">
        <input
          type="text"
          bind:value={newMessage}
          on:keydown={(e) => e.key === 'Enter' && !isLoading && sendMessage()}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button on:click={sendMessage} disabled={isLoading}>Send</button>
      </div>
    </div>
  {/if}
</main>

<style>
  main {
    height: 100vh;
    padding: 20px;
    box-sizing: border-box;
  }

  .loading-screen {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f8f9fa;
  }

  .loading-container {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 90%;
    max-width: 400px;
  }

  .loading-container h2 {
    margin: 0 0 1rem 0;
    color: #333;
    font-size: 1.2rem;
  }

  .model-info {
    margin: 1.5rem 0;
  }

  .model-name {
    margin-bottom: 1rem;
    color: #666;
    font-size: 1rem;
  }

  .progress-bar-container {
    width: 100%;
    height: 8px;
    background-color: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }

  .progress-bar {
    height: 100%;
    background-color: #007AFF;
    transition: width 0.3s ease;
  }

  .progress-text {
    color: #666;
    font-size: 0.9rem;
  }

  .error-message {
    color: #dc3545;
    padding: 1rem;
    background-color: #f8d7da;
    border-radius: 8px;
    margin: 1rem 0;
    font-size: 0.9rem;
  }

  .retry-button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #007AFF;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .retry-button:hover {
    background-color: #0056b3;
  }

  .spinner {
    width: 40px;
    height: 40px;
    margin: 1rem auto;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #007AFF;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .chat-container {
    max-width: 800px;
    margin: 0 auto;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .clear-button {
    background-color: #dc3545;
    padding: 8px 16px;
    font-size: 14px;
  }

  .clear-button:hover:not(:disabled) {
    background-color: #bb2d3b;
  }

  .messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .message {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 12px;
    word-wrap: break-word;
  }

  .message.user {
    align-self: flex-end;
    background-color: #007AFF;
    color: white;
  }

  .message.system {
    align-self: flex-start;
    background-color: #E9ECEF;
    color: black;
  }

  .loading {
    opacity: 0.7;
  }

  .input-area {
    display: flex;
    gap: 10px;
    padding: 20px 0;
  }

  input {
    flex-grow: 1;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 16px;
  }

  input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }

  button {
    padding: 12px 24px;
    background-color: #007AFF;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
  }

  button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  button:hover:not(:disabled) {
    background-color: #0056b3;
  }
</style>
