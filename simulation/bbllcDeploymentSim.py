import uuid
import time
import random

# --- Data Architecture: Core Data Entities ---

class Wallet:
    """Simulates a cryptocurrency wallet with an address and funds."""
    def __init__(self, address: str, initial_funds: float = 100.0):
        self.address = address
        self.funds = initial_funds

    def __str__(self):
        return f"Wallet(Addr: {self.address[:8]}..., Funds: {self.funds:.2f})"

class Authorization:
    """Represents complex authorizations like certifications, roles, and resource access."""
    def __init__(self, name: str, level: str = "basic", resources: list = None, certifications: list = None):
        self.name = name
        self.level = level # e.g., "basic", "certified", "admin"
        self.resources = resources if resources is not None else [] # e.g., ["cloud_gpu", "drone_fleet"]
        self.certifications = certifications if certifications is not None else [] # e.g., ["LevelA_Security", "DataScience_Expert"]

    def __str__(self):
        res_str = ", ".join(self.resources)
        cert_str = ", ".join(self.certifications)
        return f"Auth({self.name}, Level: {self.level}, Res: [{res_str}], Certs: [{cert_str}])"

class Task:
    """Represents a task posted on the blockchain."""
    def __init__(self, task_id: str, consumer_id: str, description: str,
                 required_skills: list, budget: float, deadline: int, encrypted_details: str = None):
        self.task_id = task_id
        self.consumer_id = consumer_id
        self.description = description
        self.required_skills = required_skills
        self.budget = budget
        self.deadline = deadline # Epoch time or block number
        self.encrypted_details = encrypted_details # Ciphertext of sensitive details
        self.status = "posted" # posted, bidding, negotiated, accepted, in_progress, completed, failed
        self.selected_agent_id = None
        self.bid_offers = {} # {agent_id: bid_amount}

    def __str__(self):
        return f"Task(ID: {self.task_id[:6]}..., Desc: '{self.description[:30]}...', Status: {self.status})"

class Resource:
    """Represents a specific resource available for use."""
    def __init__(self, resource_id: str, owner_id: str, resource_type: str, availability: bool = True, cost_per_unit: float = 10.0):
        self.resource_id = resource_id
        self.owner_id = owner_id
        self.resource_type = resource_type
        self.availability = availability
        self.cost_per_unit = cost_per_unit
        self.current_user = None

    def __str__(self):
        return f"Resource(ID: {self.resource_id[:6]}..., Type: {self.resource_type}, Avail: {self.availability})"

# --- Security Architecture: Simplified Encryption ---

def encrypt_data(data: str, agent_id: str) -> str:
    """Simulates encryption. In a real system, this would be asymmetric or symmetric encryption."""
    return f"ENCRYPTED_{agent_id}_{data[::-1]}" # Simple reverse + agent_id for demo

def decrypt_data(encrypted_data: str, agent_id: str) -> str:
    """Simulates decryption. Only successful if agent_id matches 'key' in ciphertext."""
    parts = encrypted_data.split('_')
    if len(parts) == 3 and parts[0] == "ENCRYPTED" and parts[1] == agent_id:
        return parts[2][::-1]
    return "[DECRYPTION FAILED]"

# --- Application Architecture: Core Components ---

class BlockchainSimulator:
    """
    Simulates a public blockchain ledger.
    Stores BB LLCs, tasks, bids, and handles "events".
    """
    def __init__(self):
        self.blocks = []
        self.current_block_height = 0
        self.bbllcs = {} # {bbllc_name: bbllc_obj}
        self.tasks = {} # {task_id: task_obj}
        self.wallets = {} # {address: wallet_obj}
        self.auths = {} # {address: auth_obj}
        self.encrypted_on_chain_data = {} # {data_hash: encrypted_payload}

    def _add_event(self, event_type: str, data: dict):
        """Internal method to add an event to the blockchain."""
        if not self.blocks:
            self.blocks.append([])
        self.blocks[-1].append({"type": event_type, "data": data, "timestamp": time.time(), "block_height": self.current_block_height})
        print(f"--- BLOCKCHAIN EVENT: {event_type} ---")
        for key, value in data.items():
            print(f"  {key}: {str(value)[:100]}")
        print("-" * 20)

    def create_bbllc(self, bbllc_name: str, initiator_address: str, governance_params: dict):
        """Simulates deploying BB LLC smart contracts."""
        if bbllc_name in self.bbllcs:
            print(f"BB LLC '{bbllc_name}' already exists on chain.")
            return False
        
        # Simulate initial wallet and authorization for the initiator
        if initiator_address not in self.wallets:
            self.wallets[initiator_address] = Wallet(initiator_address, initial_funds=1000)
            self.auths[initiator_address] = Authorization("InitiatorAuth", level="admin")

        self.bbllcs[bbllc_name] = {
            "name": bbllc_name,
            "initiator": initiator_address,
            "governance_params": governance_params,
            "status": "active",
            "treasury_wallet": Wallet(f"BBLLC_Treasury_{bbllc_name}", 500.0)
        }
        self._add_event("BBLLC_CREATED", {"name": bbllc_name, "initiator": initiator_address})
        return True

    def post_task(self, consumer_id: str, description: str, required_skills: list, budget: float, deadline: int, sensitive_details: str = None):
        """Simulates an Information Consumer posting a task."""
        task_id = str(uuid.uuid4())
        encrypted_details = None
        if sensitive_details:
            # Encrypt sensitive details for authorized agents only
            # In a real system, you might encrypt for a group of potential agents or a specific one.
            # Here, we'll just encrypt for a generic "authorized_agent" concept, or the first selected agent later.
            encrypted_details = encrypt_data(sensitive_details, "authorized_agent_placeholder")
            self.encrypted_on_chain_data[task_id] = encrypted_details # Store encrypted data with task_id as key

        task = Task(task_id, consumer_id, description, required_skills, budget, deadline, encrypted_details)
        self.tasks[task_id] = task
        self._add_event("TASK_POSTED", {"task_id": task_id, "consumer_id": consumer_id, "description_snippet": description[:50]})
        return task_id

    def record_bid(self, task_id: str, agent_id: str, bid_amount: float):
        """Simulates an agent submitting a bid for a task."""
        task = self.tasks.get(task_id)
        if task and task.status == "posted":
            task.bid_offers[agent_id] = bid_amount
            self._add_event("TASK_BID_RECORDED", {"task_id": task_id, "agent_id": agent_id, "bid_amount": bid_amount})
            return True
        return False

    def select_agent_for_task(self, task_id: str, selected_agent_id: str, negotiation_terms: dict = None):
        """Simulates a consumer selecting an agent and entering negotiation."""
        task = self.tasks.get(task_id)
        if task and task.status == "bidding":
            task.selected_agent_id = selected_agent_id
            task.status = "negotiated"
            self._add_event("AGENT_SELECTED_FOR_TASK", {"task_id": task_id, "selected_agent_id": selected_agent_id, "negotiation_terms": negotiation_terms})
            return True
        return False

    def confirm_task_acceptance(self, task_id: str, agent_id: str):
        """Simulates agent confirming acceptance after negotiation."""
        task = self.tasks.get(task_id)
        if task and task.status == "negotiated" and task.selected_agent_id == agent_id:
            task.status = "accepted"
            self._add_event("TASK_ACCEPTED", {"task_id": task_id, "agent_id": agent_id})
            return True
        return False

    def record_resource_allocation(self, task_id: str, agent_id: str, resource_id: str, duration: int):
        """Simulates recording a resource allocation on chain (or reference to it)."""
        self._add_event("RESOURCE_ALLOCATED", {"task_id": task_id, "agent_id": agent_id, "resource_id": resource_id, "duration": duration})

    def advance_block(self):
        """Simulates mining a new block."""
        self.current_block_height += 1
        self.blocks.append([])
        print(f"\n--- BLOCKCHAIN ADVANCED TO BLOCK {self.current_block_height} ---")

class AgentManagementSystem:
    """
    Manages the lifecycle of AI agents and registers human agent proxies.
    (Leveraging components like Black River's AgentForge & Nexus Weaver concepts)
    """
    def __init__(self, blockchain: BlockchainSimulator):
        self.agents = {} # {agent_id: agent_obj}
        self.blockchain = blockchain

    def provision_agent(self, agent_id: str, agent_type: str, capabilities: list, human_controlled: bool = False, initial_funds: float = 50.0):
        """Creates and registers an agent."""
        if agent_id in self.agents:
            print(f"Agent '{agent_id}' already provisioned.")
            return False
        
        agent_wallet = Wallet(agent_id + "_wallet", initial_funds)
        self.blockchain.wallets[agent_wallet.address] = agent_wallet

        agent = Agent(agent_id, agent_type, capabilities, self.blockchain, human_controlled, agent_wallet)
        self.agents[agent_id] = agent
        print(f"AMS: Provisioned {agent_type} Agent '{agent_id}'.")
        return True

    def configure_organization_graph(self, bbllc_name: str, connections: dict):
        """
        Simulates configuring the organization graph (relationships between agents).
        `connections` example: {'agent1': ['agent2', 'agent3'], 'agent2': ['agent1']}
        """
        bbllc_info = self.blockchain.bbllcs.get(bbllc_name)
        if not bbllc_info:
            print(f"AMS: BB LLC '{bbllc_name}' not found for organization configuration.")
            return False

        bbllc_info["organization_graph"] = connections
        print(f"AMS: Configured organization graph for BB LLC '{bbllc_name}'.")
        return True

class ResourceManagementSystem:
    """Manages the allocation and scheduling of external resources."""
    def __init__(self):
        self.resources = {} # {resource_id: resource_obj}

    def add_resource(self, resource: Resource):
        """Adds a resource to the system."""
        self.resources[resource.resource_id] = resource
        print(f"RMS: Added resource {resource.resource_id}.")

    def request_resource(self, resource_id: str, agent_id: str, task_id: str, duration: int) -> bool:
        """Simulates an agent requesting a resource."""
        resource = self.resources.get(resource_id)
        if resource and resource.availability:
            resource.availability = False
            resource.current_user = agent_id
            print(f"RMS: Resource {resource_id} allocated to {agent_id} for Task {task_id}.")
            return True
        print(f"RMS: Resource {resource_id} not available or not found.")
        return False

    def release_resource(self, resource_id: str):
        """Simulates an agent releasing a resource."""
        resource = self.resources.get(resource_id)
        if resource:
            resource.availability = True
            resource.current_user = None
            print(f"RMS: Resource {resource_id} released.")

class Agent:
    """Base class for AI and Human agents."""
    def __init__(self, agent_id: str, agent_type: str, capabilities: list, blockchain: BlockchainSimulator,
                 human_controlled: bool, wallet: Wallet):
        self.agent_id = agent_id
        self.agent_type = agent_type # e.g., "AI_LLM", "Human_Operator"
        self.capabilities = capabilities # e.g., ["data_analysis", "negotiation", "resource_scheduling"]
        self.blockchain = blockchain
        self.human_controlled = human_controlled
        self.wallet = wallet
        self.current_task_id = None
        print(f"Agent {self.agent_id} initialized (Type: {self.agent_type}, Human Controlled: {self.human_controlled}).")

    def monitor_blockchain_for_tasks(self):
        """Simulates agents listening for new tasks."""
        new_tasks = []
        for task_id, task in self.blockchain.tasks.items():
            if task.status == "posted" and task_id not in self.blockchain.blocks[-1]: # Simplified check for new tasks
                new_tasks.append(task)
        if new_tasks:
            print(f"Agent {self.agent_id}: Detected {len(new_tasks)} new task(s).")
        return new_tasks

    def evaluate_and_bid(self, task: Task):
        """Simulates agent evaluating a task and deciding to bid."""
        print(f"Agent {self.agent_id}: Evaluating Task {task.task_id[:6]}...")
        print(f"  Agent capabilities: {self.capabilities}")
        print(f"  Task required skills: {task.required_skills}")

        # Check if agent has at least 70% of required skills (more flexible matching)
        matching_skills = set(self.capabilities).intersection(set(task.required_skills))
        skill_match_ratio = len(matching_skills) / len(task.required_skills) if task.required_skills else 0

        print(f"  Matching skills: {matching_skills}")
        print(f"  Skill match ratio: {skill_match_ratio:.2f}")

        # More flexible bidding criteria
        can_bid = (
            skill_match_ratio >= 0.5 and  # At least 50% skill match
            self.wallet.funds >= (task.budget * 0.05) and  # Only need 5% of budget
            task.budget >= 100.0  # Minimum task value
        )

        if can_bid:
            # Bid amount based on skill match and agent confidence
            base_bid = task.budget * random.uniform(0.6, 0.9)
            skill_bonus = skill_match_ratio * 0.1  # Up to 10% bonus for perfect match
            confidence_factor = random.uniform(0.9, 1.1)  # Agent confidence variation

            bid_amount = base_bid * (1 + skill_bonus) * confidence_factor
            bid_amount = min(bid_amount, task.budget * 0.95)  # Cap at 95% of budget

            if self.blockchain.record_bid(task.task_id, self.agent_id, bid_amount):
                print(f"Agent {self.agent_id}: Bid ${bid_amount:.2f} on Task {task.task_id[:6]} (skill match: {skill_match_ratio:.1%}).")
                return True

        print(f"Agent {self.agent_id}: Decided not to bid on Task {task.task_id[:6]} (skill match: {skill_match_ratio:.1%}).")
        return False

    def participate_in_negotiation(self, task: Task, negotiation_terms: dict) -> bool:
        """Simulates agent negotiating with consumer."""
        print(f"Agent {self.agent_id}: Entering negotiation for Task {task.task_id[:6]}...")
        if self.human_controlled:
            print(f"HUMAN INTERVENTION REQUIRED for Agent {self.agent_id} on Task {task.task_id[:6]}:")
            print(f"  Task Description: {task.description}")
            print(f"  Proposed Terms: {negotiation_terms}")
            response = input("  Accept negotiation terms? (yes/no): ").lower()
            if response == 'yes':
                self.blockchain.confirm_task_acceptance(task.task_id, self.agent_id)
                self.current_task_id = task.task_id
                print(f"Agent {self.agent_id}: Accepted task {task.task_id[:6]}.")
                return True
            else:
                print(f"Agent {self.agent_id}: Rejected task {task.task_id[:6]}.")
                return False
        else: # AI Agent logic
            # For AI, simple auto-accept if terms are reasonable
            if negotiation_terms.get('payment_guarantee', False):
                self.blockchain.confirm_task_acceptance(task.task_id, self.agent_id)
                self.current_task_id = task.task_id
                print(f"Agent {self.agent_id}: AI Agent accepted task {task.task_id[:6]}.")
                return True
        return False

    def check_authorizations_and_resources(self, required_resources: list) -> dict:
        """Simulates agent checking its authorizations for required resources."""
        print(f"Agent {self.agent_id}: Checking authorizations for resources: {required_resources}...")
        available_resources = {}
        agent_auth = self.blockchain.auths.get(self.wallet.address)
        if agent_auth:
            for res_type in required_resources:
                if res_type in agent_auth.resources:
                    # In a real system, agent would discover specific resource IDs
                    # For simulation, just assume a generic resource type is "available" to it
                    available_resources[res_type] = f"resource_id_for_{res_type}" # Placeholder ID
                    print(f"Agent {self.agent_id}: Auth check PASSED for {res_type}.")
                else:
                    print(f"Agent {self.agent_id}: Auth check FAILED for {res_type}.")
        return available_resources

    def negotiate_with_resource_owner(self, resource_id: str, resource_owner: 'ResourceOwner', duration: int) -> bool:
        """Simulates agent negotiating with a resource owner."""
        print(f"Agent {self.agent_id}: Negotiating for resource {resource_id} with owner {resource_owner.owner_id}...")
        if resource_owner.request_resource_from_owner(resource_id, self.agent_id, self.current_task_id, duration):
            self.blockchain.record_resource_allocation(self.current_task_id, self.agent_id, resource_id, duration)
            print(f"Agent {self.agent_id}: Successfully acquired resource {resource_id}.")
            return True
        print(f"Agent {self.agent_id}: Failed to acquire resource {resource_id}.")
        return False

    def execute_task(self):
        """Simulates the agent performing the task."""
        if self.current_task_id:
            task = self.blockchain.tasks.get(self.current_task_id)
            if task and task.status == "accepted":
                print(f"Agent {self.agent_id}: Executing task {task.task_id[:6]}...")
                # Simulate work being done
                time.sleep(1)
                task.status = "in_progress" # Update status
                print(f"Agent {self.agent_id}: Task {task.task_id[:6]} in progress...")

                # Try to decrypt sensitive details if available
                if task.encrypted_details:
                    decrypted = decrypt_data(task.encrypted_details, self.agent_id)
                    print(f"Agent {self.agent_id}: Decrypted task details: {decrypted}")

                time.sleep(2)
                task.status = "completed" # Final status update
                print(f"Agent {self.agent_id}: Task {task.task_id[:6]} completed.")
                self.current_task_id = None # Clear current task
                return True
        print(f"Agent {self.agent_id}: No active task to execute.")
        return False

class InformationConsumer:
    """Represents an entity that posts tasks to the blockchain."""
    def __init__(self, consumer_id: str, blockchain: BlockchainSimulator):
        self.consumer_id = consumer_id
        self.blockchain = blockchain
        print(f"Information Consumer {self.consumer_id} initialized.")

    def post_new_task(self, description: str, skills: list, budget: float, deadline: int, sensitive_details: str = None):
        """Posts a new task to the blockchain simulator."""
        return self.blockchain.post_task(self.consumer_id, description, skills, budget, deadline, sensitive_details)

    def review_bids_and_negotiate(self, task_id: str):
        """Reviews bids and attempts to negotiate with agents."""
        task = self.blockchain.tasks.get(task_id)
        if not task or not task.bid_offers:
            print(f"Consumer {self.consumer_id}: No bids or task not found for {task_id[:6]}.")
            return

        print(f"Consumer {self.consumer_id}: Reviewing bids for Task {task_id[:6]}: {task.bid_offers}")
        sorted_bids = sorted(task.bid_offers.items(), key=lambda item: item[1]) # Pick lowest bid for simplicity

        if sorted_bids:
            selected_agent_id, proposed_bid = sorted_bids[0]
            print(f"Consumer {self.consumer_id}: Selecting agent {selected_agent_id} with bid {proposed_bid:.2f}.")
            task.status = "bidding" # Transition to bidding status before selection

            negotiation_terms = {"payment_guarantee": True, "deadline_flexibility": 0.1, "final_price": proposed_bid}
            if self.blockchain.select_agent_for_task(task_id, selected_agent_id, negotiation_terms):
                print(f"Consumer {self.consumer_id}: Sent negotiation terms to Agent {selected_agent_id}.")
                return selected_agent_id
        return None

class ResourceOwner:
    """Simulates an owner of resources, handling requests from agents."""
    def __init__(self, owner_id: str, rms: ResourceManagementSystem):
        self.owner_id = owner_id
        self.rms = rms
        print(f"Resource Owner {self.owner_id} initialized.")

    def request_resource_from_owner(self, resource_id: str, agent_id: str, task_id: str, duration: int) -> bool:
        """An agent directly requests a resource from this owner."""
        print(f"Resource Owner {self.owner_id}: Received request for resource {resource_id} from agent {agent_id}.")
        # Basic check if this owner actually owns the resource
        resource = self.rms.resources.get(resource_id)
        if resource and resource.owner_id == self.owner_id:
            return self.rms.request_resource(resource_id, agent_id, task_id, duration)
        print(f"Resource Owner {self.owner_id}: Resource {resource_id} not owned by me or not found in RMS.")
        return False

# --- Enhanced Simulation Functions ---

def create_multiple_tasks(blockchain: BlockchainSimulator, num_tasks: int = 5):
    """Create multiple diverse tasks to simulate a busy marketplace"""
    consumers = []
    task_ids = []

    task_templates = [
        {
            "description": "Analyze customer behavior patterns from e-commerce data",
            "skills": ["data_analysis", "machine_learning", "report_generation"],
            "budget": 750.0,
            "consumer_prefix": "ECommerce_Client"
        },
        {
            "description": "Create financial risk assessment model",
            "skills": ["statistical_modeling", "data_analysis", "visualization"],
            "budget": 900.0,
            "consumer_prefix": "FinTech_Corp"
        },
        {
            "description": "Optimize supply chain logistics using AI",
            "skills": ["optimization", "data_analysis", "project_management"],
            "budget": 1200.0,
            "consumer_prefix": "Logistics_Inc"
        },
        {
            "description": "Develop predictive maintenance algorithms",
            "skills": ["machine_learning", "data_analysis", "quality_assurance"],
            "budget": 850.0,
            "consumer_prefix": "Manufacturing_Co"
        },
        {
            "description": "Market sentiment analysis for cryptocurrency",
            "skills": ["data_analysis", "visualization", "report_generation"],
            "budget": 600.0,
            "consumer_prefix": "Crypto_Analytics"
        }
    ]

    for i in range(min(num_tasks, len(task_templates))):
        template = task_templates[i]
        consumer_id = f"{template['consumer_prefix']}_{i+1}"
        consumer = InformationConsumer(consumer_id, blockchain)
        consumers.append(consumer)

        task_id = consumer.post_new_task(
            description=template["description"],
            skills=template["skills"],
            budget=template["budget"],
            deadline=int(time.time()) + 3600 * 24 * (7 + i),  # Staggered deadlines
            sensitive_details=f"Confidential data access for {consumer_id}"
        )
        task_ids.append(task_id)

        print(f"Created task {i+1}: {template['description'][:50]}... (Budget: ${template['budget']})")

    return consumers, task_ids

def simulate_agent_lifecycle_events(ams: AgentManagementSystem, blockchain: BlockchainSimulator):
    """Simulate dynamic agent events like new registrations and capability updates"""
    print("\n--- SIMULATING AGENT LIFECYCLE EVENTS ---")

    # Add new agents dynamically
    new_agents = [
        ("AI_Agent_3", "AI_LLM", ["optimization", "mathematical_modeling", "data_analysis"]),
        ("AI_Agent_4", "AI_LLM", ["visualization", "report_generation", "statistical_modeling"]),
        ("Human_Expert_1", "Human_Operator", ["quality_assurance", "project_management", "coordination"])
    ]

    for agent_id, agent_type, capabilities in new_agents:
        if ams.provision_agent(agent_id, agent_type, capabilities, "Human" in agent_id, initial_funds=200.0):
            # Give new agents some authorizations
            auth = Authorization(f"{agent_id}_Auth", resources=["cloud_gpu"], certifications=capabilities)
            blockchain.auths[ams.agents[agent_id].wallet.address] = auth
            print(f"Added new agent: {agent_id} with capabilities: {capabilities}")

    blockchain.advance_block()

def simulate_market_dynamics(blockchain: BlockchainSimulator, consumers: list, iteration: int):
    """Simulate changing market conditions and new task postings"""
    print(f"\n--- MARKET DYNAMICS SIMULATION (Iteration {iteration}) ---")

    # Simulate market volatility affecting budgets
    market_multiplier = random.uniform(0.8, 1.3)
    print(f"Market conditions: {'Bullish' if market_multiplier > 1.0 else 'Bearish'} (multiplier: {market_multiplier:.2f})")

    # Some consumers post additional urgent tasks
    if random.random() < 0.6:  # 60% chance of urgent task
        urgent_consumer = random.choice(consumers)
        urgent_budget = 400.0 * market_multiplier

        urgent_task_id = urgent_consumer.post_new_task(
            description=f"URGENT: Quick data analysis for {urgent_consumer.consumer_id}",
            skills=["data_analysis"],
            budget=urgent_budget,
            deadline=int(time.time()) + 3600 * 2,  # 2 hours deadline
            sensitive_details="Time-sensitive market data"
        )
        print(f"URGENT TASK posted by {urgent_consumer.consumer_id}: ${urgent_budget:.2f} budget")
        return urgent_task_id

    return None

# --- Operational Architecture: Deployment Orchestration Script ---

def DeploymentOrchestrationScript(
    initiator_wallet_address: str,
    bbllc_name: str,
    initial_authorizations: dict, # {agent_id: AuthObject}
    initial_assignment_details: dict,
    blockchain: BlockchainSimulator,
    ams: AgentManagementSystem,
    rms: ResourceManagementSystem
):
    """
    Executes the automated deployment strategy for a BB LLC.
    This simulates the human interaction being limited to executing this script with parameters.
    """
    print("\n--- DEPLOYMENT ORCHESTRATION SCRIPT STARTING ---")
    print(f"Initiator: {initiator_wallet_address}")
    print(f"Deploying BB LLC: {bbllc_name}")

    # 1. Instantiate the BB LLC organization (on-chain)
    print("\n[Step 1/5] Instantiating BB LLC Smart Contracts...")
    bbllc_created = blockchain.create_bbllc(bbllc_name, initiator_wallet_address, {"voting_threshold": 0.6})
    if not bbllc_created:
        print("Deployment failed: BB LLC could not be created.")
        return

    blockchain.wallets[initiator_wallet_address] = Wallet(initiator_wallet_address, 1000) # Ensure initiator has a wallet and funds
    blockchain.auths[initiator_wallet_address] = Authorization("FoundingMember", level="admin", certifications=["BBLLC_Founder"])

    # 2. Instantiate and Configure Initial Agents
    print("\n[Step 2/5] Provisioning and Configuring Initial Agents...")
    for agent_id, auth_obj in initial_authorizations.items():
        agent_type = "AI_LLM" if "AI" in agent_id else "Human_Operator"
        ams.provision_agent(agent_id, agent_type, auth_obj.resources + auth_obj.certifications, "Human" in agent_id)
        # Assign explicit authorization object to agent's wallet
        ams.blockchain.auths[ams.agents[agent_id].wallet.address] = auth_obj

    # 3. Configure the Organization Graph (initial structure for agents)
    print("\n[Step 3/5] Configuring Initial Organization Graph...")
    initial_connections = {
        "AI_Agent_1": ["Human_Ops_Agent"],
        "Human_Ops_Agent": ["AI_Agent_1", "AI_Agent_2"],
        "AI_Agent_2": []
    }
    ams.configure_organization_graph(bbllc_name, initial_connections)

    # 4. Initiate the Assignment (post the first task)
    print("\n[Step 4/5] Initiating Initial Assignment (Posting First Task)...")
    initial_consumer = InformationConsumer("BBLLC_Initial_Consumer", blockchain)
    initial_task_id = initial_consumer.post_new_task(
        description=initial_assignment_details["description"],
        skills=initial_assignment_details["required_skills"],
        budget=initial_assignment_details["budget"],
        deadline=initial_assignment_details["deadline"],
        sensitive_details=initial_assignment_details.get("sensitive_details")
    )
    initial_consumer.task_id = initial_task_id # For later use in this script

    print(f"\nDeployment and initial assignment initiated. Task ID: {initial_task_id}")
    print("\n--- DEPLOYMENT ORCHESTRATION SCRIPT COMPLETED ---")

    return initial_consumer, initial_task_id # Return for subsequent simulation steps

# --- Simulation Execution ---

if __name__ == "__main__":
    # --- Setup Enterprise Architecture Components ---
    blockchain_simulator = BlockchainSimulator()
    ams_system = AgentManagementSystem(blockchain_simulator)
    rms_system = ResourceManagementSystem()

    # Add some initial resources to the RMS (owned by various owners)
    rms_system.add_resource(Resource("GPU_Cluster_001", "Owner_A", "cloud_gpu", True, 25.0))
    rms_system.add_resource(Resource("Drone_Fleet_001", "Owner_B", "drone_fleet", True, 15.0))
    rms_system.add_resource(Resource("Data_Science_VM_001", "Owner_C", "data_science_vm", True, 5.0))

    resource_owner_a = ResourceOwner("Owner_A", rms_system)
    resource_owner_b = ResourceOwner("Owner_B", rms_system)
    resource_owner_c = ResourceOwner("Owner_C", rms_system)

    # --- Define Deployment Parameters ---
    initiator_address_param = "0xInitiatorWalletAddr123"
    bbllc_name_param = "BlackRiverResearchDAO"

    initial_authorizations_param = {
        "AI_Agent_1": Authorization("DataProcessor", resources=["cloud_gpu", "data_science_vm"], certifications=["data_analysis", "report_generation", "machine_learning"]),
        "AI_Agent_2": Authorization("AnalyticsBot", resources=["cloud_gpu"], certifications=["data_analysis", "cloud_gpu", "statistical_modeling"]),
        "Human_Ops_Agent": Authorization("HumanSupervisor", level="admin", resources=["drone_fleet"], certifications=["report_generation", "quality_assurance", "coordination"])
    }

    initial_assignment_param = {
        "description": "Analyze market trends for Q3 2025 using financial data.",
        "required_skills": ["data_analysis", "report_generation", "cloud_gpu"],
        "budget": 500.0,
        "deadline": int(time.time()) + 3600 * 24 * 7, # 7 days from now
        "sensitive_details": "Highly confidential market data access key: XYZ789ABC"
    }

    # --- Execute the Deployment Orchestration Script ---
    print("\n--- SIMULATION SCENARIO: BB LLC DEPLOYMENT & INITIAL TASK ---")
    initial_consumer, initial_task_id = DeploymentOrchestrationScript(
        initiator_address_param,
        bbllc_name_param,
        initial_authorizations_param,
        initial_assignment_param,
        blockchain_simulator,
        ams_system,
        rms_system
    )
    print("=" * 60)

    # --- Create Additional Tasks for More Activity ---
    print("\n--- CREATING ADDITIONAL TASKS FOR ENHANCED SIMULATION ---")
    additional_consumers = []
    additional_task_ids = []

    # Create multiple diverse tasks
    task_templates = [
        {
            "description": "Analyze customer behavior patterns from e-commerce data",
            "skills": ["data_analysis", "machine_learning"],
            "budget": 750.0,
            "consumer_id": "ECommerce_Client_1"
        },
        {
            "description": "Create financial risk assessment model",
            "skills": ["data_analysis", "statistical_modeling"],
            "budget": 900.0,
            "consumer_id": "FinTech_Corp_1"
        },
        {
            "description": "Generate comprehensive market report",
            "skills": ["report_generation", "data_analysis"],
            "budget": 650.0,
            "consumer_id": "Research_Firm_1"
        }
    ]

    for template in task_templates:
        consumer = InformationConsumer(template["consumer_id"], blockchain_simulator)
        additional_consumers.append(consumer)

        task_id = consumer.post_new_task(
            description=template["description"],
            skills=template["skills"],
            budget=template["budget"],
            deadline=int(time.time()) + 3600 * 24 * 7,
            sensitive_details=f"Confidential data for {template['consumer_id']}"
        )
        additional_task_ids.append(task_id)
        print(f"Created additional task: {template['description'][:50]}... (Budget: ${template['budget']})")

    blockchain_simulator.advance_block()

    # --- Simulate Subsequent Operational Flow ---
    print("\n--- SIMULATION SCENARIO: AGENT MONITORING, BIDDING, NEGOTIATION & EXECUTION ---")

    # Get all tasks (initial + additional)
    all_task_ids = [initial_task_id] + additional_task_ids
    all_consumers = [initial_consumer] + additional_consumers

    # 1. Agents monitor blockchain for tasks
    print(f"\n1. Agents monitoring for {len(all_task_ids)} available tasks...")
    agents_in_system = list(ams_system.agents.values())

    # 2. Agents evaluate and bid on ALL available tasks
    print("\n2. Agents evaluating and bidding on all available tasks...")
    for task_id in all_task_ids:
        task = blockchain_simulator.tasks[task_id]
        print(f"\n--- BIDDING ROUND FOR TASK: {task.description[:50]}... ---")

        for agent in agents_in_system:
            agent.evaluate_and_bid(task)

        print(f"Task {task_id[:6]} received {len(task.bid_offers)} bids: {task.bid_offers}")

    blockchain_simulator.advance_block()

    # 3. Process negotiations for all tasks with bids
    print(f"\n3. Processing negotiations for all tasks with bids...")
    successful_assignments = []

    for i, (consumer, task_id) in enumerate(zip(all_consumers, all_task_ids)):
        task = blockchain_simulator.tasks[task_id]
        print(f"\n--- NEGOTIATION FOR TASK {i+1}: {task.description[:40]}... ---")

        if task.bid_offers:
            selected_agent_id = consumer.review_bids_and_negotiate(task_id)

            if selected_agent_id:
                print(f"Consumer {consumer.consumer_id} selected agent {selected_agent_id}")
                selected_agent = ams_system.agents[selected_agent_id]

                # Simplified negotiation (auto-accept for AI agents, skip human input)
                if selected_agent.human_controlled:
                    print(f"Human agent {selected_agent_id} auto-accepting for simulation purposes")
                    blockchain_simulator.confirm_task_acceptance(task_id, selected_agent_id)
                    selected_agent.current_task_id = task_id
                    negotiation_successful = True
                else:
                    negotiation_successful = selected_agent.participate_in_negotiation(
                        task, {"payment_guarantee": True, "deadline_flexibility": 0.1}
                    )

                if negotiation_successful:
                    successful_assignments.append((selected_agent, task_id, consumer))
                    print(f"✅ Task {task_id[:6]} successfully assigned to {selected_agent_id}")
                else:
                    print(f"❌ Negotiation failed for task {task_id[:6]}")
            else:
                print(f"❌ No agent selected for task {task_id[:6]}")
        else:
            print(f"❌ No bids received for task {task_id[:6]}")

    blockchain_simulator.advance_block()

    # 4. Execute all successfully assigned tasks
    print(f"\n4. Executing {len(successful_assignments)} successfully assigned tasks...")

    for selected_agent, task_id, consumer in successful_assignments:
        print(f"\n--- EXECUTING TASK {task_id[:6]} with Agent {selected_agent.agent_id} ---")

        # Simplified resource acquisition (skip detailed resource negotiation for demo)
        print(f"Agent {selected_agent.agent_id} acquiring necessary resources...")

        # Execute the task
        execution_success = selected_agent.execute_task()

        if execution_success:
            print(f"✅ Task {task_id[:6]} completed successfully by {selected_agent.agent_id}")
        else:
            print(f"❌ Task {task_id[:6]} execution failed")

        blockchain_simulator.advance_block()

    # 5. Final simulation summary
    print("\n--- ENHANCED SIMULATION SUMMARY ---")
    print(f"Total tasks created: {len(all_task_ids)}")
    print(f"Tasks with bids: {sum(1 for tid in all_task_ids if blockchain_simulator.tasks[tid].bid_offers)}")
    print(f"Successfully assigned tasks: {len(successful_assignments)}")

    print("\nFinal Task Status Summary:")
    for task_id, task in blockchain_simulator.tasks.items():
        bid_count = len(task.bid_offers)
        print(f"  {task_id[:6]}... : {task.status} | Bids: {bid_count} | Agent: {task.selected_agent_id or 'None'}")

    print("\nAgent Performance Summary:")
    for agent_id, agent in ams_system.agents.items():
        completed_tasks = sum(1 for _, tid, _ in successful_assignments if blockchain_simulator.tasks[tid].selected_agent_id == agent_id)
        print(f"  {agent_id}: {completed_tasks} tasks completed")

    print("\nFinal Agent Wallet Balances:")
    for addr, wallet in blockchain_simulator.wallets.items():
        if any(agent.wallet.address == addr for agent in ams_system.agents.values()):
            agent_name = next(agent.agent_id for agent in ams_system.agents.values() if agent.wallet.address == addr)
            print(f"  {agent_name}: ${wallet.funds:.2f}")

    print("\n--- ENHANCED SIMULATION COMPLETED ---")
