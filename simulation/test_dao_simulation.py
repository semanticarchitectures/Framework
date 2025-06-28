"""
Test script for DAO Multi-Agent Organization Simulation

This script demonstrates the simulation capabilities and tests various scenarios.
"""

import json
from dao_simulation import DAOSimulation, ProposalState, MissionStatus


def run_basic_simulation():
    """Run a basic simulation scenario"""
    print("🚀 Starting DAO Multi-Agent Organization Simulation")
    print("=" * 60)
    
    # Initialize the DAO
    dao = DAOSimulation()
    
    # Add DAO members
    print("\n📋 Adding DAO Members...")
    member1 = dao.add_member("Alice", 10000)  # High token holder
    member2 = dao.add_member("Bob", 5000)     # Medium token holder
    member3 = dao.add_member("Charlie", 2000) # Small token holder
    
    print(f"Added members: {len(dao.members)}")
    
    # Add agents with different capabilities
    print("\n🤖 Registering AI Agents...")
    agent1 = dao.add_agent("DataAnalyst_AI", ["data_analysis", "machine_learning", "reporting"])
    agent2 = dao.add_agent("WebDev_AI", ["web_development", "frontend", "backend", "database"])
    agent3 = dao.add_agent("Content_AI", ["content_creation", "writing", "social_media"])
    agent4 = dao.add_agent("Research_AI", ["research", "data_analysis", "documentation"])
    
    print(f"Registered agents: {len(dao.agents)}")
    for addr, agent in dao.agents.items():
        print(f"  - {agent.name}: {', '.join(agent.capabilities)}")
    
    # Create a proposal for a data analysis mission
    print("\n📝 Creating Governance Proposal...")
    mission_data = {
        "title": "Market Research Analysis",
        "description": "Analyze market trends and create comprehensive report",
        "required_capabilities": ["data_analysis", "research", "reporting"],
        "budget": 5000,
        "deadline_days": 21,
        "max_agents": 2
    }
    
    proposal_id = dao.create_proposal(
        proposer=member1,
        title="Proposal: Market Research Analysis Mission",
        description="Fund a comprehensive market research analysis project",
        mission_data=mission_data
    )
    
    print(f"Created proposal: {proposal_id}")
    
    # Simulate voting
    print("\n🗳️  Conducting Governance Vote...")
    dao.vote_on_proposal(proposal_id, member1, True)   # Alice votes yes
    dao.vote_on_proposal(proposal_id, member2, True)   # Bob votes yes
    dao.vote_on_proposal(proposal_id, member3, False)  # Charlie votes no
    
    proposal = dao.proposals[proposal_id]
    print(f"Voting results:")
    print(f"  For: {proposal.for_votes:.1f}")
    print(f"  Against: {proposal.against_votes:.1f}")
    
    # Finalize proposal
    success = dao.finalize_proposal(proposal_id)
    print(f"Proposal finalized: {'✅ PASSED' if success else '❌ FAILED'}")
    
    if success:
        # Find the created mission
        mission_id = None
        for mid, mission in dao.missions.items():
            if mission.title == mission_data["title"]:
                mission_id = mid
                break
        
        if mission_id:
            print(f"\n🎯 Mission Created: {mission_id}")
            
            # Assign agents to mission
            print("\n🔄 Assigning Agents to Mission...")
            assigned_agents = dao.assign_agents_to_mission(mission_id)
            
            mission = dao.missions[mission_id]
            print(f"Assigned agents:")
            for agent_addr in assigned_agents:
                agent = dao.agents[agent_addr]
                print(f"  - {agent.name} ({agent_addr})")
            
            # Simulate mission execution
            print("\n⚡ Simulating Mission Execution...")
            results = dao.simulate_mission_execution(mission_id, days_to_simulate=21)
            
            print(f"Mission outcome: {results['final_outcome'].upper()}")
            print(f"Final progress: {mission.progress:.1%}")
            print(f"Coordination events: {len(results['coordination_events'])}")
            
            # Show performance results
            print("\n📊 Agent Performance Results:")
            for agent_addr, scores in results['performance_scores'].items():
                agent = dao.agents[agent_addr]
                avg_score = sum(scores) / len(scores)
                print(f"  - {agent.name}: {avg_score:.3f} avg daily contribution")
                print(f"    New reputation: {agent.reputation:.1f}")
                print(f"    Total earnings: ${agent.total_earnings:.2f}")
    
    # Display final statistics
    print("\n📈 Final Simulation Statistics")
    print("=" * 40)
    stats = dao.get_simulation_stats()
    
    print(f"Treasury Balance: ${stats['treasury_balance']:,.2f}")
    print(f"Total Agents: {stats['total_agents']}")
    print(f"Total Members: {stats['total_members']}")
    print(f"Total Proposals: {stats['total_proposals']}")
    print(f"Total Missions: {stats['total_missions']}")
    
    print(f"\nMission Outcomes:")
    for outcome, count in stats['mission_stats'].items():
        print(f"  {outcome.replace('_', ' ').title()}: {count}")
    
    print(f"\nGovernance Results:")
    for state, count in stats['governance_stats'].items():
        print(f"  {state.replace('_', ' ').title()}: {count}")
    
    return dao, stats


def run_multi_mission_simulation():
    """Run a more complex simulation with multiple missions"""
    print("\n\n🔄 Running Multi-Mission Simulation")
    print("=" * 60)
    
    dao = DAOSimulation()
    
    # Add members and agents
    members = []
    for i, (name, balance) in enumerate([("Alice", 15000), ("Bob", 8000), ("Charlie", 5000), ("Diana", 3000)]):
        member_id = dao.add_member(name, balance)
        members.append(member_id)
    
    agents = []
    agent_configs = [
        ("AI_Researcher", ["research", "data_analysis", "documentation"]),
        ("AI_Developer", ["web_development", "backend", "database"]),
        ("AI_Designer", ["frontend", "ui_design", "user_experience"]),
        ("AI_Writer", ["content_creation", "writing", "documentation"]),
        ("AI_Analyst", ["data_analysis", "machine_learning", "reporting"]),
        ("AI_Marketer", ["social_media", "content_creation", "marketing"])
    ]
    
    for name, capabilities in agent_configs:
        agent_id = dao.add_agent(name, capabilities)
        agents.append(agent_id)
    
    # Create multiple proposals
    missions_data = [
        {
            "title": "Website Development Project",
            "description": "Build a new company website with modern design",
            "required_capabilities": ["web_development", "frontend", "ui_design"],
            "budget": 8000,
            "deadline_days": 30,
            "max_agents": 3
        },
        {
            "title": "Content Marketing Campaign",
            "description": "Create comprehensive content marketing strategy",
            "required_capabilities": ["content_creation", "social_media", "marketing"],
            "budget": 4000,
            "deadline_days": 14,
            "max_agents": 2
        },
        {
            "title": "Data Science Analysis",
            "description": "Perform advanced analytics on customer data",
            "required_capabilities": ["data_analysis", "machine_learning"],
            "budget": 6000,
            "deadline_days": 25,
            "max_agents": 2
        }
    ]
    
    proposal_ids = []
    for i, mission_data in enumerate(missions_data):
        proposal_id = dao.create_proposal(
            proposer=members[i % len(members)],
            title=f"Proposal: {mission_data['title']}",
            description=mission_data['description'],
            mission_data=mission_data
        )
        proposal_ids.append(proposal_id)
    
    print(f"Created {len(proposal_ids)} proposals")
    
    # Simulate voting on all proposals
    for proposal_id in proposal_ids:
        # Simulate different voting patterns
        for member_id in members:
            vote = True if dao.members[member_id].token_balance > 5000 else (hash(proposal_id + member_id) % 2 == 0)
            dao.vote_on_proposal(proposal_id, member_id, vote)
        
        # Finalize proposal
        success = dao.finalize_proposal(proposal_id)
        proposal = dao.proposals[proposal_id]
        print(f"Proposal '{proposal.title}': {'PASSED' if success else 'FAILED'}")
    
    # Execute all successful missions
    mission_results = {}
    for mission_id, mission in dao.missions.items():
        if mission.status == MissionStatus.CREATED:
            assigned_agents = dao.assign_agents_to_mission(mission_id)
            if assigned_agents:
                print(f"\nExecuting mission: {mission.title}")
                results = dao.simulate_mission_execution(mission_id)
                mission_results[mission_id] = results
                print(f"  Outcome: {results['final_outcome']}")
    
    # Final statistics
    stats = dao.get_simulation_stats()
    print(f"\n📊 Multi-Mission Simulation Results:")
    print(f"Successful missions: {stats['mission_stats']['success']}")
    print(f"Failed missions: {stats['mission_stats']['failure']}")
    print(f"Treasury remaining: ${stats['treasury_balance']:,.2f}")
    
    # Top performing agents
    print(f"\n🏆 Top Performing Agents:")
    agent_performance = [(addr, data['avg_performance']) for addr, data in stats['agent_stats'].items()]
    agent_performance.sort(key=lambda x: x[1], reverse=True)
    
    for i, (addr, performance) in enumerate(agent_performance[:3]):
        agent_data = stats['agent_stats'][addr]
        print(f"  {i+1}. {agent_data['name']}: {performance:.3f} avg performance, ${agent_data['total_earnings']:.2f} earned")
    
    return dao, stats


if __name__ == "__main__":
    # Run basic simulation
    dao1, stats1 = run_basic_simulation()
    
    # Run multi-mission simulation
    dao2, stats2 = run_multi_mission_simulation()
    
    print("\n✅ Simulation Complete!")
    print("\nThis simulation demonstrates:")
    print("- DAO governance with token-weighted voting")
    print("- Agent registration and capability matching")
    print("- Mission assignment and execution")
    print("- Performance tracking and reputation systems")
    print("- Economic incentives and reward distribution")
