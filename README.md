# LocalChat

*A local chat room created using socket and thread in Python.*

**How to use:**

<ul>
  <li>Run the  <code>server.py</code>  by providing the <code>host address</code> and <code>port number</code>. Host address can be your <code>localhost</code> or your local area network's address or can be a public IP address if you've access to.
  Care must be taken to choose a port that is currently not in usage.
  If no <code>host</code> & <code>port</code> are provided, it'll run the server by default at <code>localhost:54321</code>.</li>
  <br>
 <li>Every user must run the <code>client.py</code> script individually on the same address(<code>host:port</code>) as the server is running on to connect to the chatroom. Again, if no <code>host</code> & <code>port</code> are provided, it'll try to connect by default to <code>localhost:54321</code></li>
</ul>

**To Do:**
<ul>
  <li> Add Chatting App like GUI using Kivy.
</ul>
