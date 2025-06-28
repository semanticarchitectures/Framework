"""
DAO Multi-Agent Organization Simulation

This simulation models the core functionality of a DAO-operated multi-agent organization
to test governance, agent coordination, mission assignment, and economic models.
"""

import random
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum
import json
from datetime import datetime, timedelta


class ProposalState(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUCCEEDED = "succeeded"
    DEFEATED = "defeated"
    EXECUTED = "executed"


class MissionStatus(Enum):
    CREATED = "created"
    AGENT_SELECTION = "agent_selection"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Agent:
    """Represents an AI agent in the organization"""
    address: str
    name: str
    capabilities: Set[str]
    reputation: float = 100.0
    staked_amount: float = 0.0
    performance_history: List[Dict] = field(default_factory=list)
    active_missions: Set[str] = field(default_factory=set)
    total_earnings: float = 0.0
    
    def can_perform_mission(self, required_capabilities: Set[str]) -> bool:
        """Check if agent has required capabilities for a mission"""
        return required_capabilities.issubset(self.capabilities)
    
    def get_capability_score(self, capability: str) -> float:
        """Get agent's proficiency score for a specific capability"""
        if capability not in self.capabilities:
            return 0.0
        
        # Calculate score based on performance history
        relevant_performances = [
            p['score'] for p in self.performance_history 
            if capability in p.get('capabilities_used', [])
        ]
        
        if not relevant_performances:
            return 0.5  # Default score for new capabilities
        
        return sum(relevant_performances) / len(relevant_performances)


@dataclass
class DAOMember:
    """Represents a DAO member with voting rights"""
    address: str
    name: str
    token_balance: float
    reputation: float = 100.0
    voting_history: List[Dict] = field(default_factory=list)
    
    def get_voting_power(self) -> float:
        """Calculate voting power based on tokens and reputation"""
        return self.token_balance * (self.reputation / 100.0)


@dataclass
class Proposal:
    """Represents a DAO governance proposal"""
    id: str
    proposer: str
    title: str
    description: str
    mission_data: Dict
    voting_start: datetime
    voting_end: datetime
    state: ProposalState = ProposalState.PENDING
    for_votes: float = 0.0
    against_votes: float = 0.0
    votes: Dict[str, Dict] = field(default_factory=dict)


@dataclass
class Mission:
    """Represents a mission assigned to agents"""
    id: str
    title: str
    description: str
    required_capabilities: Set[str]
    budget: float
    deadline: datetime
    max_agents: int
    assigned_agents: List[str] = field(default_factory=list)
    status: MissionStatus = MissionStatus.CREATED
    progress: float = 0.0
    results: Optional[Dict] = None
    coordination_messages: List[Dict] = field(default_factory=list)


class DAOSimulation:
    """Main simulation class for the DAO multi-agent organization"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.members: Dict[str, DAOMember] = {}
        self.proposals: Dict[str, Proposal] = {}
        self.missions: Dict[str, Mission] = {}
        self.treasury_balance: float = 1000000.0  # Starting treasury
        self.current_time: datetime = datetime.now()
        
        # Simulation parameters
        self.voting_period_days = 7
        self.minimum_quorum = 0.1  # 10% of voting power
        self.success_threshold = 0.5  # 50% of votes
        
    def add_agent(self, name: str, capabilities: List[str], stake: float = 1000.0) -> str:
        """Register a new agent in the DAO"""
        address = f"agent_{uuid.uuid4().hex[:8]}"
        agent = Agent(
            address=address,
            name=name,
            capabilities=set(capabilities),
            staked_amount=stake
        )
        self.agents[address] = agent
        return address
    
    def add_member(self, name: str, token_balance: float) -> str:
        """Add a new DAO member"""
        address = f"member_{uuid.uuid4().hex[:8]}"
        member = DAOMember(
            address=address,
            name=name,
            token_balance=token_balance
        )
        self.members[address] = member
        return address
    
    def create_proposal(self, proposer: str, title: str, description: str, 
                       mission_data: Dict) -> str:
        """Create a new governance proposal"""
        proposal_id = f"prop_{uuid.uuid4().hex[:8]}"
        
        proposal = Proposal(
            id=proposal_id,
            proposer=proposer,
            title=title,
            description=description,
            mission_data=mission_data,
            voting_start=self.current_time,
            voting_end=self.current_time + timedelta(days=self.voting_period_days),
            state=ProposalState.ACTIVE
        )
        
        self.proposals[proposal_id] = proposal
        return proposal_id
    
    def vote_on_proposal(self, proposal_id: str, voter: str, support: bool) -> bool:
        """Cast a vote on a proposal"""
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        if proposal.state != ProposalState.ACTIVE:
            return False
        
        if voter not in self.members:
            return False
        
        member = self.members[voter]
        voting_power = member.get_voting_power()
        
        # Record the vote
        proposal.votes[voter] = {
            'support': support,
            'voting_power': voting_power,
            'timestamp': self.current_time
        }
        
        if support:
            proposal.for_votes += voting_power
        else:
            proposal.against_votes += voting_power
        
        # Update member's voting history
        member.voting_history.append({
            'proposal_id': proposal_id,
            'support': support,
            'timestamp': self.current_time
        })
        
        return True
    
    def finalize_proposal(self, proposal_id: str) -> bool:
        """Finalize a proposal after voting period"""
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        if proposal.state != ProposalState.ACTIVE:
            return False
        
        total_votes = proposal.for_votes + proposal.against_votes
        total_voting_power = sum(m.get_voting_power() for m in self.members.values())
        
        # Check quorum
        if total_votes < total_voting_power * self.minimum_quorum:
            proposal.state = ProposalState.DEFEATED
            return False
        
        # Check if proposal passed
        if proposal.for_votes > proposal.against_votes and \
           proposal.for_votes > total_votes * self.success_threshold:
            proposal.state = ProposalState.SUCCEEDED
            return self.execute_proposal(proposal_id)
        else:
            proposal.state = ProposalState.DEFEATED
            return False
    
    def execute_proposal(self, proposal_id: str) -> bool:
        """Execute a successful proposal by creating a mission"""
        proposal = self.proposals[proposal_id]
        if proposal.state != ProposalState.SUCCEEDED:
            return False
        
        mission_data = proposal.mission_data
        mission_id = self.create_mission(
            title=mission_data['title'],
            description=mission_data['description'],
            required_capabilities=set(mission_data['required_capabilities']),
            budget=mission_data['budget'],
            deadline_days=mission_data.get('deadline_days', 30),
            max_agents=mission_data.get('max_agents', 3)
        )
        
        proposal.state = ProposalState.EXECUTED
        return mission_id is not None
    
    def create_mission(self, title: str, description: str, 
                      required_capabilities: Set[str], budget: float,
                      deadline_days: int = 30, max_agents: int = 3) -> str:
        """Create a new mission"""
        mission_id = f"mission_{uuid.uuid4().hex[:8]}"
        
        mission = Mission(
            id=mission_id,
            title=title,
            description=description,
            required_capabilities=required_capabilities,
            budget=budget,
            deadline=self.current_time + timedelta(days=deadline_days),
            max_agents=max_agents
        )
        
        self.missions[mission_id] = mission
        return mission_id
    
    def assign_agents_to_mission(self, mission_id: str) -> List[str]:
        """Automatically assign best-suited agents to a mission"""
        if mission_id not in self.missions:
            return []
        
        mission = self.missions[mission_id]
        if mission.status != MissionStatus.CREATED:
            return []
        
        # Find qualified agents
        qualified_agents = []
        for agent in self.agents.values():
            if agent.can_perform_mission(mission.required_capabilities):
                # Calculate agent score for this mission
                capability_scores = [
                    agent.get_capability_score(cap) 
                    for cap in mission.required_capabilities
                ]
                avg_capability_score = sum(capability_scores) / len(capability_scores)
                
                # Factor in reputation and availability
                availability_bonus = 1.0 if len(agent.active_missions) == 0 else 0.8
                total_score = (avg_capability_score * 0.6 + 
                              agent.reputation / 100.0 * 0.4) * availability_bonus
                
                qualified_agents.append((agent.address, total_score))
        
        # Sort by score and select top agents
        qualified_agents.sort(key=lambda x: x[1], reverse=True)
        selected_agents = [addr for addr, _ in qualified_agents[:mission.max_agents]]
        
        # Assign agents to mission
        mission.assigned_agents = selected_agents
        mission.status = MissionStatus.IN_PROGRESS
        
        # Update agent active missions
        for agent_addr in selected_agents:
            self.agents[agent_addr].active_missions.add(mission_id)
        
        return selected_agents

    def simulate_mission_execution(self, mission_id: str, days_to_simulate: int = 30) -> Dict:
        """Simulate mission execution over time"""
        if mission_id not in self.missions:
            return {}

        mission = self.missions[mission_id]
        if mission.status != MissionStatus.IN_PROGRESS:
            return {}

        # Simulation parameters
        daily_progress_base = 1.0 / days_to_simulate  # Base progress per day
        coordination_bonus = 0.1  # Bonus for good coordination

        results = {
            'daily_progress': [],
            'coordination_events': [],
            'performance_scores': {},
            'final_outcome': None
        }

        for day in range(days_to_simulate):
            # Calculate daily progress based on agent performance
            daily_progress = 0.0

            for agent_addr in mission.assigned_agents:
                agent = self.agents[agent_addr]

                # Agent's contribution based on capabilities and reputation
                capability_match = len(mission.required_capabilities.intersection(agent.capabilities)) / len(mission.required_capabilities)
                agent_contribution = daily_progress_base * capability_match * (agent.reputation / 100.0)

                # Add some randomness for realistic simulation
                randomness_factor = random.uniform(0.8, 1.2)
                agent_contribution *= randomness_factor

                daily_progress += agent_contribution

                # Track individual performance
                if agent_addr not in results['performance_scores']:
                    results['performance_scores'][agent_addr] = []
                results['performance_scores'][agent_addr].append(agent_contribution)

            # Coordination events (random)
            if random.random() < 0.3:  # 30% chance of coordination event
                coordination_event = {
                    'day': day,
                    'type': random.choice(['planning', 'problem_solving', 'resource_sharing']),
                    'participants': random.sample(mission.assigned_agents,
                                                min(2, len(mission.assigned_agents))),
                    'effectiveness': random.uniform(0.5, 1.0)
                }
                results['coordination_events'].append(coordination_event)

                # Coordination bonus
                daily_progress += coordination_bonus * coordination_event['effectiveness']

            mission.progress += daily_progress
            results['daily_progress'].append(daily_progress)

            # Check if mission is complete
            if mission.progress >= 1.0:
                mission.status = MissionStatus.COMPLETED
                break

        # Determine final outcome
        if mission.progress >= 1.0:
            results['final_outcome'] = 'success'
            mission.status = MissionStatus.COMPLETED
        elif mission.progress >= 0.7:
            results['final_outcome'] = 'partial_success'
            mission.status = MissionStatus.COMPLETED
        else:
            results['final_outcome'] = 'failure'
            mission.status = MissionStatus.FAILED

        # Update agent performance and reputation
        self._update_agent_performance(mission_id, results)

        # Distribute rewards
        self._distribute_mission_rewards(mission_id, results)

        return results

    def _update_agent_performance(self, mission_id: str, results: Dict):
        """Update agent performance records and reputation"""
        mission = self.missions[mission_id]

        for agent_addr in mission.assigned_agents:
            agent = self.agents[agent_addr]

            # Calculate agent's performance score
            agent_contributions = results['performance_scores'].get(agent_addr, [])
            avg_contribution = sum(agent_contributions) / len(agent_contributions) if agent_contributions else 0

            # Normalize to 0-1 scale
            performance_score = min(1.0, avg_contribution * len(mission.assigned_agents))

            # Bonus for successful mission completion
            if results['final_outcome'] == 'success':
                performance_score *= 1.2
            elif results['final_outcome'] == 'partial_success':
                performance_score *= 1.1

            # Record performance
            performance_record = {
                'mission_id': mission_id,
                'score': performance_score,
                'capabilities_used': list(mission.required_capabilities),
                'timestamp': self.current_time,
                'outcome': results['final_outcome']
            }
            agent.performance_history.append(performance_record)

            # Update reputation (exponential moving average)
            reputation_change = (performance_score - 0.5) * 10  # -5 to +5 change
            agent.reputation = agent.reputation * 0.9 + (agent.reputation + reputation_change) * 0.1
            agent.reputation = max(0, min(200, agent.reputation))  # Clamp between 0-200

            # Remove from active missions
            agent.active_missions.discard(mission_id)

    def _distribute_mission_rewards(self, mission_id: str, results: Dict):
        """Distribute rewards to agents based on performance"""
        mission = self.missions[mission_id]

        if results['final_outcome'] == 'failure':
            return  # No rewards for failed missions

        # Calculate reward multiplier based on outcome
        reward_multiplier = {
            'success': 1.0,
            'partial_success': 0.7
        }.get(results['final_outcome'], 0)

        total_reward = mission.budget * reward_multiplier

        # Calculate individual rewards based on performance
        total_performance = sum(
            sum(scores) for scores in results['performance_scores'].values()
        )

        if total_performance > 0:
            for agent_addr in mission.assigned_agents:
                agent = self.agents[agent_addr]
                agent_performance = sum(results['performance_scores'].get(agent_addr, []))
                agent_reward = total_reward * (agent_performance / total_performance)

                agent.total_earnings += agent_reward

                # Deduct from treasury
                self.treasury_balance -= agent_reward

    def get_simulation_stats(self) -> Dict:
        """Get comprehensive simulation statistics"""
        stats = {
            'treasury_balance': self.treasury_balance,
            'total_agents': len(self.agents),
            'total_members': len(self.members),
            'total_proposals': len(self.proposals),
            'total_missions': len(self.missions),
            'agent_stats': {},
            'mission_stats': {},
            'governance_stats': {}
        }

        # Agent statistics
        for addr, agent in self.agents.items():
            stats['agent_stats'][addr] = {
                'name': agent.name,
                'reputation': agent.reputation,
                'total_earnings': agent.total_earnings,
                'missions_completed': len(agent.performance_history),
                'avg_performance': sum(p['score'] for p in agent.performance_history) / len(agent.performance_history) if agent.performance_history else 0,
                'capabilities': list(agent.capabilities)
            }

        # Mission statistics
        mission_outcomes = {'success': 0, 'partial_success': 0, 'failure': 0, 'in_progress': 0}
        for mission in self.missions.values():
            if mission.status == MissionStatus.COMPLETED:
                # Determine outcome based on progress
                if mission.progress >= 1.0:
                    mission_outcomes['success'] += 1
                elif mission.progress >= 0.7:
                    mission_outcomes['partial_success'] += 1
                else:
                    mission_outcomes['failure'] += 1
            elif mission.status == MissionStatus.FAILED:
                mission_outcomes['failure'] += 1
            else:
                mission_outcomes['in_progress'] += 1

        stats['mission_stats'] = mission_outcomes

        # Governance statistics
        proposal_outcomes = {'succeeded': 0, 'defeated': 0, 'active': 0, 'executed': 0}
        for proposal in self.proposals.values():
            proposal_outcomes[proposal.state.value] += 1

        stats['governance_stats'] = proposal_outcomes

        return stats
