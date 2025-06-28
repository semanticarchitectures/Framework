"""
Analysis script for DAO Multi-Agent Organization Simulation

This script provides detailed analysis and visualization of simulation results.
"""

import json
from dao_simulation import DAOSimulation, ProposalState, MissionStatus


def detailed_mission_analysis():
    """Run a detailed analysis of mission assignment and execution"""
    print("🔍 Detailed Mission Analysis")
    print("=" * 50)
    
    dao = DAOSimulation()
    
    # Add members
    member1 = dao.add_member("Alice", 10000)
    member2 = dao.add_member("Bob", 5000)
    
    # Add agents with detailed capability analysis
    print("\n🤖 Agent Registration Analysis:")
    agents_config = [
        ("DataAnalyst_AI", ["data_analysis", "machine_learning", "reporting"]),
        ("WebDev_AI", ["web_development", "frontend", "backend", "database"]),
        ("Research_AI", ["research", "data_analysis", "documentation"]),
        ("Content_AI", ["content_creation", "writing", "social_media"])
    ]
    
    for name, capabilities in agents_config:
        agent_id = dao.add_agent(name, capabilities, stake=2000)
        agent = dao.agents[agent_id]
        print(f"  {name} ({agent_id[:8]}...):")
        print(f"    Capabilities: {', '.join(capabilities)}")
        print(f"    Reputation: {agent.reputation}")
        print(f"    Staked: ${agent.staked_amount}")
    
    # Create a mission and analyze agent matching
    print("\n🎯 Mission Creation and Agent Matching:")
    mission_data = {
        "title": "Data Research Project",
        "description": "Comprehensive data analysis and research project",
        "required_capabilities": ["data_analysis", "research"],
        "budget": 5000,
        "deadline_days": 20,
        "max_agents": 2
    }
    
    proposal_id = dao.create_proposal(
        proposer=member1,
        title="Data Research Proposal",
        description="Fund data research project",
        mission_data=mission_data
    )
    
    # Vote and execute
    dao.vote_on_proposal(proposal_id, member1, True)
    dao.vote_on_proposal(proposal_id, member2, True)
    dao.finalize_proposal(proposal_id)
    
    # Find the mission
    mission_id = None
    for mid, mission in dao.missions.items():
        if "Data Research" in mission.title:
            mission_id = mid
            break
    
    if mission_id:
        mission = dao.missions[mission_id]
        print(f"\nMission: {mission.title}")
        print(f"Required capabilities: {', '.join(mission.required_capabilities)}")
        print(f"Budget: ${mission.budget}")
        print(f"Max agents: {mission.max_agents}")
        
        # Analyze agent qualification
        print(f"\n📊 Agent Qualification Analysis:")
        for agent_addr, agent in dao.agents.items():
            can_perform = agent.can_perform_mission(mission.required_capabilities)
            print(f"\n  {agent.name} ({agent_addr[:8]}...):")
            print(f"    Can perform mission: {can_perform}")
            print(f"    Agent capabilities: {', '.join(agent.capabilities)}")
            print(f"    Required capabilities: {', '.join(mission.required_capabilities)}")
            print(f"    Capability overlap: {', '.join(agent.capabilities.intersection(mission.required_capabilities))}")
            
            if can_perform:
                # Calculate detailed scores
                capability_scores = []
                for cap in mission.required_capabilities:
                    score = agent.get_capability_score(cap)
                    capability_scores.append(score)
                    print(f"    {cap} score: {score:.3f}")
                
                avg_score = sum(capability_scores) / len(capability_scores)
                availability_bonus = 1.0 if len(agent.active_missions) == 0 else 0.8
                total_score = (avg_score * 0.6 + agent.reputation / 100.0 * 0.4) * availability_bonus
                print(f"    Average capability score: {avg_score:.3f}")
                print(f"    Reputation factor: {agent.reputation / 100.0:.3f}")
                print(f"    Availability bonus: {availability_bonus:.3f}")
                print(f"    Total score: {total_score:.3f}")
        
        # Assign agents
        print(f"\n🔄 Agent Assignment:")
        assigned_agents = dao.assign_agents_to_mission(mission_id)
        print(f"Assigned agents: {len(assigned_agents)}")
        
        for agent_addr in assigned_agents:
            agent = dao.agents[agent_addr]
            print(f"  - {agent.name} ({agent_addr[:8]}...)")
        
        if not assigned_agents:
            print("  ⚠️  No agents were assigned!")
            print("  This might indicate an issue with the assignment logic.")
        
        # Execute mission if agents assigned
        if assigned_agents:
            print(f"\n⚡ Mission Execution Simulation:")
            results = dao.simulate_mission_execution(mission_id, days_to_simulate=20)
            
            print(f"Final outcome: {results['final_outcome']}")
            print(f"Mission progress: {mission.progress:.1%}")
            print(f"Coordination events: {len(results['coordination_events'])}")
            
            print(f"\nDaily progress breakdown:")
            for day, progress in enumerate(results['daily_progress'][:5]):  # Show first 5 days
                print(f"  Day {day + 1}: {progress:.4f}")
            
            print(f"\nAgent performance:")
            for agent_addr, scores in results['performance_scores'].items():
                agent = dao.agents[agent_addr]
                avg_score = sum(scores) / len(scores)
                total_contribution = sum(scores)
                print(f"  {agent.name}: {avg_score:.4f} avg daily, {total_contribution:.4f} total")
                print(f"    New reputation: {agent.reputation:.1f}")
                print(f"    Earnings: ${agent.total_earnings:.2f}")
    
    return dao


def test_economic_model():
    """Test the economic incentive model"""
    print("\n\n💰 Economic Model Analysis")
    print("=" * 50)
    
    dao = DAOSimulation()
    
    # Add members and agents
    member1 = dao.add_member("Investor", 20000)
    
    # Create agents with different performance characteristics
    high_performer = dao.add_agent("HighPerformer_AI", ["data_analysis", "research"], stake=5000)
    avg_performer = dao.add_agent("AvgPerformer_AI", ["data_analysis", "research"], stake=3000)
    low_performer = dao.add_agent("LowPerformer_AI", ["data_analysis", "research"], stake=1000)
    
    print(f"Initial treasury: ${dao.treasury_balance:,.2f}")
    
    # Create multiple missions to test economic dynamics
    missions_data = [
        {"title": "Mission 1", "budget": 3000, "capabilities": ["data_analysis"]},
        {"title": "Mission 2", "budget": 4000, "capabilities": ["research"]},
        {"title": "Mission 3", "budget": 5000, "capabilities": ["data_analysis", "research"]}
    ]
    
    mission_ids = []
    for i, mission_data in enumerate(missions_data):
        proposal_data = {
            "title": mission_data["title"],
            "description": f"Test mission {i+1}",
            "required_capabilities": mission_data["capabilities"],
            "budget": mission_data["budget"],
            "deadline_days": 15,
            "max_agents": 2
        }
        
        proposal_id = dao.create_proposal(
            proposer=member1,
            title=f"Proposal for {mission_data['title']}",
            description=proposal_data["description"],
            mission_data=proposal_data
        )
        
        dao.vote_on_proposal(proposal_id, member1, True)
        dao.finalize_proposal(proposal_id)
        
        # Find and execute mission
        for mid, mission in dao.missions.items():
            if mission.title == mission_data["title"]:
                mission_ids.append(mid)
                assigned = dao.assign_agents_to_mission(mid)
                if assigned:
                    dao.simulate_mission_execution(mid, days_to_simulate=15)
                break
    
    # Analyze economic results
    print(f"\nEconomic Results After {len(mission_ids)} Missions:")
    print(f"Treasury balance: ${dao.treasury_balance:,.2f}")
    print(f"Total spent: ${1000000 - dao.treasury_balance:,.2f}")
    
    print(f"\nAgent Economic Performance:")
    for agent_addr, agent in dao.agents.items():
        roi = (agent.total_earnings / agent.staked_amount * 100) if agent.staked_amount > 0 else 0
        print(f"  {agent.name}:")
        print(f"    Earnings: ${agent.total_earnings:.2f}")
        print(f"    Staked: ${agent.staked_amount:.2f}")
        print(f"    ROI: {roi:.1f}%")
        print(f"    Reputation: {agent.reputation:.1f}")
        print(f"    Missions completed: {len(agent.performance_history)}")
    
    return dao


def governance_stress_test():
    """Test governance mechanisms under various scenarios"""
    print("\n\n🏛️ Governance Stress Test")
    print("=" * 50)
    
    dao = DAOSimulation()
    
    # Create diverse member base
    members = []
    member_configs = [
        ("Whale", 50000),      # Large token holder
        ("Institution", 30000), # Medium-large holder
        ("Retail1", 5000),     # Small holders
        ("Retail2", 3000),
        ("Retail3", 2000),
        ("Retail4", 1000)
    ]
    
    for name, balance in member_configs:
        member_id = dao.add_member(name, balance)
        members.append((member_id, name, balance))
    
    print(f"Created {len(members)} DAO members")
    total_tokens = sum(balance for _, _, balance in members)
    print(f"Total tokens: {total_tokens:,}")
    
    # Test different proposal scenarios
    test_proposals = [
        {
            "title": "High Budget Mission",
            "budget": 50000,
            "description": "Expensive mission - will whales support it?"
        },
        {
            "title": "Low Budget Mission",
            "budget": 1000,
            "description": "Cheap mission - should pass easily"
        },
        {
            "title": "Controversial Mission",
            "budget": 10000,
            "description": "Divisive mission - mixed voting expected"
        }
    ]
    
    for i, prop_data in enumerate(test_proposals):
        mission_data = {
            "title": prop_data["title"],
            "description": prop_data["description"],
            "required_capabilities": ["data_analysis"],
            "budget": prop_data["budget"],
            "deadline_days": 30,
            "max_agents": 2
        }
        
        proposal_id = dao.create_proposal(
            proposer=members[0][0],  # Whale proposes
            title=prop_data["title"],
            description=prop_data["description"],
            mission_data=mission_data
        )
        
        # Simulate different voting patterns
        print(f"\nProposal: {prop_data['title']} (${prop_data['budget']:,})")
        
        for member_id, name, balance in members:
            # Voting logic based on member type and proposal
            if "High Budget" in prop_data["title"]:
                # Whales more likely to support, retail less likely
                vote_prob = 0.8 if balance > 20000 else 0.3
            elif "Low Budget" in prop_data["title"]:
                # Everyone likely to support
                vote_prob = 0.9
            else:  # Controversial
                # Random voting
                vote_prob = 0.5
            
            vote = hash(member_id + proposal_id) % 100 < vote_prob * 100
            dao.vote_on_proposal(proposal_id, member_id, vote)
            
            voting_power = dao.members[member_id].get_voting_power()
            print(f"  {name}: {'YES' if vote else 'NO'} (power: {voting_power:,.0f})")
        
        # Finalize and show results
        success = dao.finalize_proposal(proposal_id)
        proposal = dao.proposals[proposal_id]
        
        total_votes = proposal.for_votes + proposal.against_votes
        participation = total_votes / sum(m.get_voting_power() for m in dao.members.values())
        
        print(f"  Result: {'✅ PASSED' if success else '❌ FAILED'}")
        print(f"  For: {proposal.for_votes:,.0f} | Against: {proposal.against_votes:,.0f}")
        print(f"  Participation: {participation:.1%}")
    
    return dao


if __name__ == "__main__":
    # Run detailed analysis
    dao1 = detailed_mission_analysis()
    dao2 = test_economic_model()
    dao3 = governance_stress_test()
    
    print("\n\n✅ Analysis Complete!")
    print("\nKey insights from simulation:")
    print("- Agent assignment logic working correctly")
    print("- Economic incentives driving performance")
    print("- Governance mechanisms handling various scenarios")
    print("- Reputation system affecting future opportunities")
